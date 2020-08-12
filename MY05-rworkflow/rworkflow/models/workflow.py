from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from .base import BaseModel
from .state import State


class Workflow(BaseModel):
    """工作流"""

    name = models.CharField(_('名称'), max_length=128)
    code = models.CharField(_('编号'), max_length=40, null=True, blank=True)
    ################################################################
    # 关联的对象
    ################################################################
    content_type = models.ForeignKey(
        ContentType,
        verbose_name=_('Content Type'),
        on_delete=models.PROTECT,
        db_constraint=False,
        related_name='+',
    )
    object_id = models.PositiveIntegerField(_('对象ID'), blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    app_label = models.CharField(_('应用名称'), max_length=128, blank=True, null=True)
    model_name = models.CharField(_('模型名称'), max_length=128, blank=True, null=True)

    ORC_ALLORDER = '00'
    ORC_SELECT = '10'
    ORC_DEFAULT = ORC_ALLORDER
    ORC_CHOICES = (
        (ORC_ALLORDER, '通过Content Type配置给所有工单'),
        (ORC_SELECT, '通过工单外键主动选择工作流'),
    )
    order_relation_config = models.CharField(
        _('工作流与工单的关系配置'),
        max_length=16,
        choices=ORC_CHOICES,
        default=ORC_DEFAULT,
    )

    ################################################################
    # 状态
    ################################################################
    # 初始状态
    # initial_state = models.ForeignKey(
    #     'State', verbose_name=_('初始状态'),
    #     on_delete=models.PROTECT,
    #     db_constraint=False,
    #     blank=True, null=True,
    #     related_name='workflow_this_set_as_initial_state',
    # )

    # field_name = models.CharField(_('状态字段'), max_length=128, blank=True, null=True)
    # 状态字段
    status_field = models.CharField(_('状态字段'), max_length=128, blank=True, null=True)
    # 初始状态值
    init_status_value = models.CharField(_('初始状态值'), max_length=128, blank=True, null=True)

    category = models.ForeignKey(
        'WorkflowCategory',
        verbose_name=_('类别'),
        null=True, blank=True,
        on_delete=models.SET_NULL,
        db_constraint=False,
        related_name='workflows',
    )
    ################################################################
    # 状态信息
    ################################################################
    # 是否在用
    is_active = models.BooleanField(_('在用？'), default=True)
    # 排序权重
    weight = models.IntegerField(_('排序权重'), blank=True, null=True, default=99)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('工作流程')
        verbose_name_plural = _('工作流程')
        # content_type 和 field_name 是唯一字段
        # unique_together = [("content_type", "field_name")]

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.content_type:
            self.app_label = self.content_type.app_label
            self.model_name = self.content_type.model
        super().save(force_insert, force_update, using, update_fields)

    def get_initial_state(self):
        try:
            init_state = self.states.filter(is_start=True).first()
        except State.DoesNotExist:
            init_state = self.states.order('weight', 'code',).first()
        return init_state
