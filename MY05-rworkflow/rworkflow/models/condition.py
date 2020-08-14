
import logging
from django.conf import settings

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from .base import BaseModel
from . import extraparam


VALUE_TP_CHOICES = (
    (extraparam.BOOL, _('布尔值')),
    (extraparam.INT, _('整型值')),
    (extraparam.BIGINT, _('大整型值')),
    (extraparam.POSINT, _('正整型值')),
    (extraparam.FLOAT, _('浮点值')),
    (extraparam.DECIMAL, _('定点值')),
)
VALUE_TP_DEFAULT = VALUE_TP_CHOICES[0][0]


class ConditionMeta(BaseModel):
    """流转条件元数据"""

    workflow = models.ForeignKey(
        'Workflow',
        verbose_name=_('工作流程'),
        on_delete=models.CASCADE,
        db_constraint=False,
        related_name='condition_metas',
    )

    name = models.CharField(_('名称'), max_length=80)
    code = models.CharField(_('编号'), max_length=40, default='', blank=True)
    is_active = models.BooleanField(_('在用？'), default=True)
    weight = models.IntegerField(_('排序权重'), blank=True, null=True, default=9)

    OPERATOR_CHOICES = (
        ('=', _('等于')),
        ('>', _('大于')),
        ('<', _('小于')),
        ('<=', _('大于等于')),
        ('>=', _('小于等于')),
    )
    operator = models.CharField(
        _('操作符'),
        max_length=15,
        choices=OPERATOR_CHOICES,
    )

    extraparam_meta = models.ForeignKey(
        'ExtraParamMeta',
        verbose_name=_('参数元数据'),
        on_delete=models.CASCADE,
        db_constraint=False,
        related_name='condition_metas',
    )
    extraparam_meta_right = models.ForeignKey(
        'ExtraParamMeta',
        verbose_name=_('参数元数据右值'),
        on_delete=models.CASCADE,
        db_constraint=False,
        related_name='condition_metas_right',
    )

    VALUE_TP_CHOICES = VALUE_TP_CHOICES
    VALUE_TP_DEFAULT = VALUE_TP_DEFAULT
    value_tp = models.CharField(
        _('值类型'),
        max_length=40,
        # blank=True, null=True,
        choices=VALUE_TP_CHOICES,
        default=VALUE_TP_DEFAULT,
    )

    bool_value = models.BooleanField(_('布尔值'), null=True, blank=True)
    int_value = models.IntegerField(_('整型值'), null=True, blank=True)
    bigint_value = models.BigIntegerField(_('大整型值'), null=True, blank=True)
    posint_value = models.PositiveIntegerField(_('正整型值'), null=True, blank=True)
    float_value = models.FloatField(_('浮点值'), null=True, blank=True)
    decimal_value = models.DecimalField(_('定点值'), max_digits=14, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('条件元数据')
        verbose_name_plural = _('条件元数据')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        if not self.code:
            self.code = 'CO%03d' % self.id
            self.save(update_fields=['code'])


class Condition(models.Model):
    """流转条件"""

    workflow = models.ForeignKey(
        'Workflow',
        verbose_name=_('工作流程'),
        on_delete=models.CASCADE,
        db_constraint=False,
        related_name='condition_metas',
    )

    meta = models.ForeignKey(
        ConditionMeta,
        verbose_name=_('流转条件元数据'),
        on_delete=models.CASCADE,
        db_constraint=False,
    )

    name = models.CharField(_('名称'), max_length=80)
    weight = models.IntegerField(_('排序权重'), blank=True, null=True, default=9)
    created_at = models.DateTimeField(_('创建时间'), null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), null=True, blank=True, auto_now=True)

    # 以 extraparam_meta 为基础创建的 参数 赋值到这里
    extraparam = models.ForeignKey(
        'ExtraParam',
        verbose_name=_('参数'),
        on_delete=models.CASCADE,
        db_constraint=False,
        related_name='conditions',
    )
    # 以 extraparam_meta_right 为基础创建的 参数 赋值到这里
    extraparam_right = models.ForeignKey(
        'ExtraParam',
        verbose_name=_('参数右值'),
        on_delete=models.CASCADE,
        db_constraint=False,
        related_name='conditions_right',
    )

    OPERATOR_CHOICES = (
        ('=', _('等于')),
        ('>', _('大于')),
        ('<', _('小于')),
        ('<=', _('大于等于')),
        ('>=', _('小于等于')),
    )
    operator = models.CharField(
        _('操作符'),
        max_length=15,
        choices=OPERATOR_CHOICES,
    )

    VALUE_TP_CHOICES = VALUE_TP_CHOICES
    VALUE_TP_DEFAULT = VALUE_TP_DEFAULT
    value_tp = models.CharField(
        _('值类型'),
        max_length=40,
        # blank=True, null=True,
        choices=VALUE_TP_CHOICES,
        default=VALUE_TP_DEFAULT,
    )

    bool_value = models.BooleanField(_('布尔值'), null=True, blank=True)
    int_value = models.IntegerField(_('整型值'), null=True, blank=True)
    bigint_value = models.BigIntegerField(_('大整型值'), null=True, blank=True)
    posint_value = models.PositiveIntegerField(_('正整型值'), null=True, blank=True)
    float_value = models.FloatField(_('浮点值'), null=True, blank=True)
    decimal_value = models.DecimalField(_('定点值'), max_digits=14, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('流转条件')
        verbose_name_plural = _('流转条件')
