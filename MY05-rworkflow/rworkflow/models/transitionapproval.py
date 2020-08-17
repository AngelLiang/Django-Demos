import logging

from django.conf import settings
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey

from .base import BaseModel
from ..managers import TransitionApprovalManager

LOGGER = logging.getLogger(__name__)


class TransitionApproval(models.Model):
    """流转批准"""

    CODE_PREFIX = 'TA'
    CODE_NUMBER_WIDTH = 8

    name = models.CharField(_('名称'), max_length=80, default='', blank=True)
    code = models.CharField(_('编号'), max_length=40, default='', blank=True)

    # 关联的对象
    content_type = models.ForeignKey(
        ContentType,
        verbose_name=_('Content Type'),
        on_delete=models.CASCADE,
        db_constraint=False,
        related_name='+',
    )
    object_id = models.PositiveIntegerField(_('对象ID'), blank=True, null=True)
    workflow_object = GenericForeignKey('content_type', 'object_id')

    # 元数据
    meta = models.ForeignKey(
        'TransitionApprovalMeta',
        verbose_name=_('元数据'),
        null=True, blank=True,
        on_delete=models.SET_NULL,
        db_constraint=False,
        related_name="transition_approvals",
    )
    # 工作流
    workflow = models.ForeignKey(
        'Workflow',
        verbose_name=_('工作流程'),
        on_delete=models.PROTECT,
        db_constraint=False,
        related_name='transition_approvals',
    )

    # 关联的流转
    transition = models.ForeignKey(
        'Transition',
        verbose_name=_('关联的流转'),
        on_delete=models.PROTECT,
        db_constraint=False,
        related_name='transition_approvals',
    )

    # 流转者
    transactioner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('处理者'),
        db_constraint=False,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    # 流转日期时间
    transaction_at = models.DateTimeField(_('处理时间'), null=True, blank=True)
    memo = models.TextField(_('处理意见'), max_length=10000, default='')

    PENDING = "pending"
    APPROVED = "approved"
    JUMPED = "jumped"
    CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (PENDING, _('准备中')),
        (APPROVED, _('已处理')),
        (CANCELLED, _('已取消')),
        (JUMPED, _('已跳转')),
    ]
    # 流转批准状态
    status = models.CharField(_('状态'), max_length=16, choices=STATUS_CHOICES, default=PENDING, db_index=True)

    # # 权限
    # permissions = models.ManyToManyField(Permission, verbose_name=_('权限'))
    # # 权限组
    # groups = models.ManyToManyField(Group, verbose_name=_('权限组'))

    priority = models.IntegerField(_('优先级'), default=0)
    weight = models.IntegerField(_('排序权重'), blank=True, null=True, default=9)

    # 前一个流转
    # previous = TreeOneToOneField(
    previous = models.OneToOneField(
        'self', verbose_name=_('前一个批准'),
        related_name="next_transition",
        null=True, blank=True,
        on_delete=models.CASCADE,
        db_constraint=False,
    )

    created_at = models.DateTimeField(_('创建时间'), null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), null=True, blank=True, auto_now=True)

    ################################################################
    can_edit = models.BooleanField(_('处理人可编辑？'), default=False)
    can_suggestion = models.BooleanField(_('处理人可填写处理意见？'), default=False)
    is_suggestion_required = models.BooleanField(_('处理意见是否必填？'), default=False)
    need_take = models.BooleanField(_('需要处理人接单？'), default=False)

    ################################################################
    # 通知字段
    ################################################################
    # 邮件通知
    email_notice = models.BooleanField(_('邮件通知'), default=True)
    # 短信通知
    short_message_notice = models.BooleanField(_('短信通知'), default=False)
    # 微信通知
    weixin_notice = models.BooleanField(_('微信通知'), default=False)

    ################################################################
    # 指定处理人字段
    ################################################################
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('处理人'),
        db_constraint=False,
        blank=True,
        related_name='transition_approvals',
    )

    def __str__(self):
        return f'{self.meta} - {self.status}'

    class Meta:
        verbose_name = _('流程批准')
        verbose_name_plural = _('流程批准')

    objects = TransitionApprovalManager()

    @property
    def peers(self):
        return TransitionApproval.objects.filter(
            workflow_object=self.workflow_object,
            workflow=self.workflow,
            transition=self.transition,
        ).exclude(pk=self.pk)
