
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .base import BaseModel
# from common import const


class State(BaseModel):
    """状态"""

    # 工作流
    workflow = models.ForeignKey(
        'Workflow',
        verbose_name=_('工作流程'),
        on_delete=models.CASCADE,
        db_constraint=False,
        related_name='states',
    )

    ################################################################
    # 基本字段
    ################################################################
    name = models.CharField(_('名称'), max_length=80)
    code = models.CharField(_('编号'), max_length=80, null=True, blank=True)

    is_start = models.BooleanField(_('起始状态？'), default=False)
    is_stop = models.BooleanField(_('结束状态？'), default=False)
    can_edit = models.BooleanField(_('可编辑？'), default=False)
    can_take = models.BooleanField(_('可接单？'), default=False)

    status_field = models.CharField(_('状态字段'), max_length=40, blank=True, null=True)
    status_value = models.CharField(_('状态值'), max_length=40, blank=True, null=True)

    ################################################################
    # 状态信息
    ################################################################
    # 是否在用
    is_active = models.BooleanField(_('在用？'), default=True)
    # 排序权重
    weight = models.IntegerField(_('权重'), blank=True, null=True, default=99)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('流程状态')
        verbose_name_plural = _('流程状态')
        ordering = ('workflow', 'weight', 'code')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        if not self.code:
            self.code = 'S%03d' % self.id
            self.save(update_fields=['code'])

    def get_status_field(self):
        if self.status_field:
            return self.status_field
        return self.workflow.status_field
