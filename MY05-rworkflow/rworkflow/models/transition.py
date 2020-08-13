import logging

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey

from .base import BaseModel
from ..managers import TransitionApprovalManager

LOGGER = logging.getLogger(__name__)


class Transition(models.Model):
    """流转"""

    name = models.CharField(_('名称'), max_length=80, default='', blank=True)
    code = models.CharField(_('编号'), max_length=40, default='', blank=True)

    content_type = models.ForeignKey(
        ContentType,
        verbose_name=_('Content Type'),
        on_delete=models.CASCADE,
        db_constraint=False,
        related_name='+',
    )
    object_id = models.PositiveIntegerField(_('关联的对象ID'), blank=True, null=True)
    # 通用外键
    workflow_object = GenericForeignKey('content_type', 'object_id')

    # 流转元数据
    meta = models.ForeignKey(
        'TransitionMeta',
        verbose_name=_('元数据'),
        on_delete=models.PROTECT,
        db_constraint=False,
        related_name="transitions",
    )
    # 工作流
    workflow = models.ForeignKey(
        'Workflow',
        verbose_name=_("工作流"),
        on_delete=models.PROTECT,
        db_constraint=False,
        related_name='transitions',
    )
    # 初始状态
    source_state = models.ForeignKey(
        'State', verbose_name=_('初始状态'),
        on_delete=models.PROTECT,
        db_constraint=False,
        related_name='transition_as_source',
    )
    # 目的状态
    destination_state = models.ForeignKey(
        'State', verbose_name=_('目的状态'),
        on_delete=models.PROTECT,
        db_constraint=False,
        related_name='transition_as_destination',
    )

    # source_state_value = models.CharField(
    #     _('初始状态值'),
    #     max_length=40,
    #     blank=True, null=True,
    # )
    # destination_state_value = models.CharField(
    #     _('目的状态值'),
    #     max_length=40,
    #     blank=True, null=True,
    # )

    PENDING = "pending"
    CANCELLED = "cancelled"
    DONE = "done"
    JUMPED = "jumped"

    STATUS_CHOICES = (
        (PENDING, _('准备中')),
        (CANCELLED, _('已取消')),
        (DONE, _('已完成')),
        (JUMPED, _('已跳转')),
    )
    # 状态
    status = models.CharField(_('状态'), max_length=16, choices=STATUS_CHOICES, default=PENDING, db_index=True)

    iteration = models.IntegerField(_('迭代层级'), default=0)

    @property
    def next_transitions(self):
        """下一个流转"""
        return Transition.objects.filter(
            workflow=self.workflow,
            workflow_object=self.workflow_object,
            source_state=self.destination_state,  # 源状态=目的状态
            iteration=self.iteration + 1
        )

    @property
    def peers(self):
        return Transition.objects.filter(
            workflow=self.workflow,
            workflow_object=self.workflow_object,
            source_state=self.source_state,
            iteration=self.iteration
        ).exclude(pk=self.pk)

    class Meta:
        verbose_name = _('流程流转')
        verbose_name_plural = _('流程流转')
        # default_permissions = ('view', 'change')

    objects = TransitionApprovalManager()
