import logging

from django.conf import settings
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey

from mptt.models import MPTTModel
from mptt.fields import TreeOneToOneField

from .base import BaseModel
from ..managers import TransitionApprovalManager

LOGGER = logging.getLogger(__name__)


class TransitionApproval(BaseModel):
    """流转批准"""

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
        verbose_name=_('工作流'),
        on_delete=models.PROTECT,
        db_constraint=False,
        related_name='transition_approvals',
    )

    # 关联的流转
    transition = models.ForeignKey(
        'Transition',
        verbose_name=_('流转'),
        on_delete=models.PROTECT,
        db_constraint=False,
        related_name='transition_approvals',
    )

    # 流转者
    transactioner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('流转者'),
        db_constraint=False,
        null=True, blank=True,
        on_delete=models.SET_NULL,
    )
    # 流转日期时间
    transaction_at = models.DateTimeField(null=True, blank=True)

    PENDING = "pending"
    APPROVED = "approved"
    JUMPED = "jumped"
    CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (PENDING, _('Pending')),
        (APPROVED, _('Approved')),
        (CANCELLED, _('Cancelled')),
        (JUMPED, _('Jumped')),
    ]
    # 流转批准状态
    status = models.CharField(_('状态'), max_length=16, choices=STATUS_CHOICES, default=PENDING)

    # 权限
    permissions = models.ManyToManyField(Permission, verbose_name=_('权限'))
    # 权限组
    groups = models.ManyToManyField(Group, verbose_name=_('权限组'))

    # 优先级
    priority = models.IntegerField(_('优先级'), default=0)
    # 前一个流转
    # previous = TreeOneToOneField(
    previous = models.OneToOneField(
        'self', verbose_name=_('前一个流转'),
        related_name="next_transition",
        null=True, blank=True,
        on_delete=models.CASCADE,
        db_constraint=False,
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
