import logging
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth import get_user_model

from .base import BaseModel
from .fields.state import StateField

from .workflow_instance import WorkflowInstance

User = get_user_model()
LOGGER = logging.getLogger(__name__)


class Wforder(BaseModel):
    """工单"""
    title = models.CharField(_('工单标题'), max_length=128)
    code = models.CharField(_('工单编号'), max_length=40, default='')

    # TP_CHOICES = (
    #     ('00', '加班申请'),
    #     ('10', '调休申请'),
    #     ('20', '假期申请'),
    # )
    # tp = models.CharField(
    #     _('工单类型'),
    #     max_length=16,
    #     blank=True, null=True,
    #     choices=TP_CHOICES,
    #     # default='D'
    # )

    description = models.TextField(
        _('描述'), max_length=10000,
        blank=True, null=True,
    )

    # 状态
    status = models.CharField(
        _('状态'),
        max_length=40,
        blank=True, null=True,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('申请者'),
        blank=True, null=True,
        on_delete=models.CASCADE,
        db_constraint=False,
        related_name='+',
    )

    # related_users = models.ManyToManyField(
    #     settings.AUTH_USER_MODEL,
    #     verbose_name=_('相关人员'),
    #     db_constraint=False,
    #     related_name='+',
    #     # related_name='related_%(app_label)s_%(class)s',
    # )

    workflow_category = models.ForeignKey(
        'WorkflowCategory',
        verbose_name=_('流程类别'),
        null=True, blank=True,
        on_delete=models.PROTECT,
        db_constraint=False,
    )
    workflow = models.ForeignKey(
        'Workflow',
        verbose_name=_('工单流程'),
        null=True, blank=True,
        on_delete=models.PROTECT,
        db_constraint=False,
    )
    workflow_instance = models.ForeignKey(
        'WorkflowInstance',
        verbose_name=_('流程实例'),
        null=True, blank=True,
        on_delete=models.SET_NULL,
        db_constraint=False,
    )
    rstatus = StateField(
        verbose_name=_('状态'),
        blank=True, null=True,
        on_delete=models.PROTECT,
        db_constraint=False,
    )

    def __str__(self):
        return f'{self.code} - {self.title}'

    class Meta:
        verbose_name = _('工单')
        verbose_name_plural = _('工单')

    def applier(self):
        if self.user:
            username = self.user.get_username()
            fullname = self.user.get_full_name()
            value = username
            if fullname:
                value += f'（{fullname}）'
            return value
        return ''
    applier.short_description = _('申请人')

    def can_edit(self):
        status = self.get_status()
        return status and status.can_edit

    def can_suggestion(self):
        status = self.get_status()
        return status and status.can_suggestion

    def is_suggestion_required(self):
        status = self.get_status()
        return status and status.is_suggestion_required

    def need_take(self):
        status = self.get_status()
        return status and status.need_take

    def is_wf_start(self):
        workflow_instance = self.get_workflow_instance()
        return workflow_instance and workflow_instance.is_wf_start()

    def is_wf_finish(self):
        workflow_instance = self.get_workflow_instance()
        return workflow_instance and workflow_instance.is_wf_finish()

    def is_on_initial_state(self):
        workflow_instance = self.get_workflow_instance()
        return workflow_instance and workflow_instance.on_initial_state

    def get_current_handle_users(self):
        users = []
        workflow_instance = self.get_workflow_instance()
        if workflow_instance:
            approvals = workflow_instance.get_next_approvals()
            tempusers = User.objects.filter(transition_approvals__in=approvals).all()
            users.extend(tempusers)
        return users

    def is_current_handle_user(self, user):
        workflow_instance = self.get_workflow_instance()
        if workflow_instance:
            approvals = workflow_instance.get_next_approvals()
            return User.objects.filter(
                transition_approvals__in=approvals, id=user.id
            ).exists()
        return False

    def get_status(self):
        return self.rstatus

    def set_status(self, value):
        self.rstatus = value

    def get_workflow(self):
        return self.workflow

    def get_workflow_instance(self):
        return self.workflow_instance

    def get_next_approvals(self):
        """获取下一批准集合"""
        workflow_instance = self.get_workflow_instance()
        if workflow_instance:
            return workflow_instance.get_next_approvals()

    def get_recent_approval(self):
        """获取最近的批准"""
        workflow_instance = self.get_workflow_instance()
        if workflow_instance:
            return workflow_instance.get_recent_approval()

    def get_history_approvals(self):
        """获取历史批准数据"""
        workflow_instance = self.get_workflow_instance()
        if workflow_instance:
            return workflow_instance.get_history_approvals()

    # def get_common_workflow(self):
    #     opts = self._meta
    #     app_label = opts.app_label
    #     model_name = opts.model_name

    #     WORKFLOW_APP_LABEL = 'rworkflow'
    #     WORKFLOW_MODEL_NAME = 'workflow'
    #     try:
    #         content_type = ContentType.objects.get(app_label=WORKFLOW_APP_LABEL, model=WORKFLOW_MODEL_NAME)
    #         workflow = content_type.get_object_for_this_type(app_label=app_label, model_name=model_name)
    #     except Exception:
    #         return None
    #     return workflow

    def get_workflow_instance_from_content_type(self):
        workflow = self.get_workflow()
        workflow_instance = WorkflowInstance.objects.get(
            workflow=workflow, object_id=self.id
        )
        return workflow_instance

    def get_or_create_workflow_instance(self, request):
        workflow = self.get_workflow()
        if not workflow:
            return None, None
        workflow_instance, is_created = WorkflowInstance.objects.get_or_create(
            workflow=workflow, object_id=self.id, starter=request.user
        )
        self.workflow_instance = workflow_instance
        self.save(update_fields=['workflow_instance'])
        return workflow_instance, is_created

    def wf_start(self, request):
        """启动工作流程"""
        workflow = self.workflow
        if not workflow:
            raise ValueError('没有配置工作流程')

        workflow_instance = self.get_workflow_instance()
        if not workflow_instance:
            workflow_instance = self.get_workflow_instance_from_content_type()
        if not workflow_instance:
            workflow_instance, is_created = self.get_or_create_workflow_instance(request=request)

        # init_status_value = workflow.init_status_value
        # workflow_instance.set_state(init_status_value)
        if workflow_instance:
            # 提交之后再初始化
            workflow_instance.initialize_approvals(request)
        return True

    def initialize_status(self):
        """如果当前状态不是所配的工作流的初始状态，并且工作流也没有启动，则设置该初始状态"""
        if self.workflow and not self.is_wf_start():
            status = self.workflow.get_initial_state()
            if self.get_status() is not status:
                self.set_status(status)

    def gen_code(self):
        """code为空的时候自动生成"""
        if not self.code:
            self.code = 'WO%05d' % self.id
            self.save(update_fields=['code'])

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.initialize_status()
        super().save(force_insert, force_update, using, update_fields)
        self.gen_code()
