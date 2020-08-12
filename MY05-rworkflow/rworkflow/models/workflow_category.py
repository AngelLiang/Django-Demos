from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from .base import BaseModel


class WorkflowCategory(BaseModel):

    ################################################################
    # 基本字段
    ################################################################
    name = models.CharField(_('名称'), max_length=80)
    code = models.CharField(_('编号'), max_length=40, default='', blank=True)
    short = models.CharField(_('简称'), max_length=80, default='', blank=True)
    pinyin = models.CharField(_('拼音/英文'), max_length=128, default='', blank=True)
    spec = models.CharField(_('简单描述'), max_length=255, default='', blank=True)

    # 是否在用
    is_active = models.BooleanField(_('在用？'), default=True)
    weight = models.IntegerField(_('排序权重'), default=99)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('流程分类')
        verbose_name_plural = _('流程分类')
        ordering = ('weight', 'code',)
