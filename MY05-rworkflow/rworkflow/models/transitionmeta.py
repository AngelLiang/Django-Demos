from django.db import models
from django.utils.translation import ugettext_lazy as _

from .base import BaseModel


class TransitionMeta(BaseModel):
    """流转元数据"""

    # 工作流
    workflow = models.ForeignKey(
        'Workflow', verbose_name=_("工作流"),
        on_delete=models.CASCADE,
        db_constraint=False,
        related_name='transition_metas',
    )

    # 初始状态
    source_state = models.ForeignKey(
        'State', verbose_name=_('初始状态'),
        on_delete=models.PROTECT,
        db_constraint=False,
        related_name='transition_meta_as_source',
    )
    # 目的状态
    destination_state = models.ForeignKey(
        'State', verbose_name=_('目的状态'),
        related_name='transition_meta_as_destination',
        on_delete=models.PROTECT,
        db_constraint=False,
    )

    source_state_value = models.CharField(
        _('初始状态值'),
        max_length=40,
        blank=True, null=True,
    )
    destination_state_value = models.CharField(
        _('目的状态值'),
        max_length=40,
        blank=True, null=True,
    )

    # 权重
    weight = models.IntegerField(_('权重'), blank=True, null=True, default=99)

    def __str__(self):
        return '工作流:%s, %s -> %s' % (
            self.workflow,
            self.source_state,
            self.destination_state
        )

    class Meta:
        verbose_name = _('流转元数据')
        verbose_name_plural = _('流转元数据')
        unique_together = (('workflow', 'source_state', 'destination_state'))
        ordering = ('workflow', 'weight',)
