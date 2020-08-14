import logging
from django.conf import settings

from django.db import models
from django.utils.translation import ugettext_lazy as _

from .base import BaseModel
from ..managers import EatraParamManager

BOOL = 'bool'
CHAR = 'char'
TEXT = 'text'
INT = 'int'
BIGINT = 'bigint'
POSINT = 'posint'
FLOAT = 'float'
BINARY = 'binary'
DECIMAL = 'decimal'
TIME = 'time'
DATE = 'date'
DATETIME = 'datetime'
DURATION = 'duration'
FILE = 'file'
IMAGE = 'image'
CHOICE = 'choice'
MULTIPLE_CHOICE = 'multiple_choice'
VALUE_TP_CHOICES = (
    (BOOL, _('布尔值')),
    (CHAR, _('字符串')),
    (TEXT, _('文本值')),
    (INT, _('整型值')),
    (BIGINT, _('大整型值')),
    (POSINT, _('正整型值')),
    (FLOAT, _('浮点值')),
    (BINARY, _('二进制值')),
    (DECIMAL, _('定点值')),
    (TIME, _('时间值')),
    (DATE, _('日期值')),
    (DATETIME, _('日期时间值')),
    (DURATION, _('时间间隔值')),
    (FILE, _('文件')),
    (IMAGE, _('图片')),

    (CHOICE, _('单选值')),
    (MULTIPLE_CHOICE, _('多选值')),
)
VALUE_TP_DEFAULT = VALUE_TP_CHOICES[0][0]


class ExtraParamMeta(BaseModel):
    """额外参数元数据"""

    workflow = models.ForeignKey(
        'Workflow',
        verbose_name=_('工作流程'),
        on_delete=models.CASCADE,
        db_constraint=False,
        related_name='extra_param_metas',
    )

    name = models.CharField(_('名称'), max_length=80)
    code = models.CharField(_('编号'), max_length=40, default='', blank=True)
    is_active = models.BooleanField(_('在用？'), default=True)
    memo = models.CharField(_('备注'), max_length=255, default='', blank=True)

    VALUE_TP_CHOICES = VALUE_TP_CHOICES
    VALUE_TP_DEFAULT = VALUE_TP_DEFAULT
    value_tp = models.CharField(
        _('值类型'),
        max_length=40,
        # blank=True, null=True,
        choices=VALUE_TP_CHOICES,
        default=VALUE_TP_DEFAULT,
    )
    is_choice_combo = models.BooleanField(_('choice控件是否以combo方式选择'), default=False)
    is_choice_async = models.BooleanField(_('choice控件是否异步加载'), default=False)

    # 排序权重
    weight = models.IntegerField(_('排序权重'), blank=True, null=True, default=9)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('额外参数元数据')
        verbose_name_plural = _('额外参数元数据')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        if not self.code:
            self.code = 'EX%03d' % self.id
            self.save(update_fields=['code'])


class ExtraParam(models.Model):
    """额外参数"""

    # 工作流
    wo = models.ForeignKey(
        'Wforder',
        verbose_name=_('工单'),
        on_delete=models.CASCADE,
        db_constraint=False,
        related_name='extra_params',
    )

    # 元数据
    meta = models.ForeignKey(
        ExtraParamMeta,
        verbose_name=_('元数据'),
        null=True, blank=True,
        on_delete=models.SET_NULL,
        db_constraint=False,
        related_name='extra_params',
    )

    ################################################################
    # 基础信息
    name = models.CharField(_('名称'), max_length=80)
    memo = models.CharField(_('备注'), max_length=255, default='', blank=True)
    created_at = models.DateTimeField(_('创建时间'), null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), null=True, blank=True, auto_now=True)

    ################################################################
    # 值类型和具体数据
    VALUE_TP_CHOICES = VALUE_TP_CHOICES
    VALUE_TP_DEFAULT = VALUE_TP_DEFAULT
    value_tp = models.CharField(
        _('值类型'),
        max_length=40,
        # blank=True, null=True,
        choices=VALUE_TP_CHOICES,
        default=VALUE_TP_DEFAULT,
    )

    # 字符串型
    bool_value = models.BooleanField(_('布尔值'), null=True, blank=True)
    # 电话号码、IP等数值可用该字段
    char_value = models.CharField(_('字符串值'), max_length=255, null=True, blank=True)
    # 邮箱、URL等数值可用该字段
    text_value = models.TextField(_('文本值'), null=True, blank=True)
    # 数值型
    int_value = models.IntegerField(_('整型值'), null=True, blank=True)
    bigint_value = models.BigIntegerField(_('大整型值'), null=True, blank=True)
    posint_value = models.PositiveIntegerField(_('正整型值'), null=True, blank=True)
    float_value = models.FloatField(_('浮点值'), null=True, blank=True)
    binary_value = models.BinaryField(_('二进制值'), null=True, blank=True)
    decimal_value = models.DecimalField(_('定点值'), max_digits=14, decimal_places=6, null=True, blank=True)
    # 时间
    time_value = models.TimeField(_('时间值'), null=True, blank=True)
    date_value = models.DateField(_('日期值'), null=True, blank=True)
    datetime_value = models.DateTimeField(_('日期时间值'), null=True, blank=True)
    duration_value = models.DurationField(_('时间间隔值'), null=True, blank=True)
    # 文件
    file_value = models.FileField(_('文件'), null=True, blank=True)
    image_value = models.ImageField(_('图片'), null=True, blank=True)

    choice_value = models.CharField(_('单选值'), max_length=255, null=True, blank=True)
    multiple_choice_value = models.TextField(_('多选值'), null=True, blank=True)

    ################################################################

    is_choice_combo = models.BooleanField(_('choice控件是否以combo方式选择'), default=False)
    is_choice_async = models.BooleanField(_('choice控件是否异步加载'), default=False)

    # 排序权重
    weight = models.IntegerField(_('排序权重'), blank=True, null=True, default=9)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('额外参数')
        verbose_name_plural = _('额外参数')

    objects = EatraParamManager()

    def get_value(self):
        tp = self.value_tp
        return getattr(self, f'{tp}_value', None)

    def set_value(self, value):
        tp = self.value_tp
        return setattr(self, f'{tp}_value', value)

    value = property(get_value, set_value)


class ExtraParamChoiceMeta(BaseModel):
    """参数选择值元数据"""

    extra_param_meta = models.ForeignKey(
        ExtraParamMeta,
        verbose_name=_('额外参数元数据'),
        null=True, blank=True,
        on_delete=models.CASCADE,
        db_constraint=False,
        related_name='extra_param_metas',
    )

    name = models.CharField(_('名称'), max_length=80)
    display_value = models.CharField(_('数值'), max_length=255, default='', blank=True)

    # 排序权重
    weight = models.IntegerField(_('排序权重'), blank=True, null=True, default=9)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('参数选择值元数据')
        verbose_name_plural = _('参数选择值元数据')


class ExtraParamChoice(BaseModel):
    """参数选择值"""

    meta = models.ForeignKey(
        ExtraParamChoiceMeta,
        verbose_name=_('元数据'),
        null=True, blank=True,
        on_delete=models.SET_NULL,
        db_constraint=False,
        related_name='extra_param_choices',
    )

    extra_param = models.ForeignKey(
        ExtraParam,
        verbose_name=_('额外参数'),
        null=True, blank=True,
        on_delete=models.CASCADE,
        db_constraint=False,
        related_name='extra_param_choices',
    )

    name = models.CharField(_('名称'), max_length=80)
    display_value = models.CharField(_('数值'), max_length=255, default='', blank=True)

    # 排序权重
    weight = models.IntegerField(_('排序权重'), blank=True, null=True, default=9)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('参数选择值')
        verbose_name_plural = _('参数选择值')
