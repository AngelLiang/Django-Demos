import logging
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.contenttypes.fields import GenericRelation

from .base import BaseModel
from .fields.state import StateField

from .workflow_instance import WorkflowInstance

LOGGER = logging.getLogger(__name__)


class Wforder(BaseModel):
    """工单"""
    code = models.CharField(_('工单编号'), max_length=80, null=True, blank=True)
    title = models.CharField(_('工单标题'), max_length=128)

    TP_CHOICES = (
        ('00', '加班申请'),
        ('10', '调休申请'),
        ('20', '假期申请'),
    )
    tp = models.CharField(
        _('工单类型'),
        max_length=16,
        blank=True, null=True,
        choices=TP_CHOICES,
        # default='D'
    )

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
    )

    # workflow = models.ForeignKey(
    #     'Workflow',
    #     verbose_name=_('工作流程'),
    #     blank=True, null=True,
    #     on_delete=models.PROTECT,
    #     db_constraint=False,
    #     limit_choices_to={'order_relation_config': '10'},
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

    def can_edit(self):
        return self.rstatus is None or (self.rstatus and self.rstatus.can_edit)

    def is_wf_start(self):
        return self.rstatus is not None

    def get_status(self):
        return self.rstatus

    def get_workflow(self):
        return self.workflow

    def get_workflow_instance(self):
        return self.workflow_instance

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
            workflow_instance.initialize_approvals()
        return True
