from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from .base import BaseModel
from .fields.state import StateField
# from common import const


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

    workflow = models.ForeignKey(
        'Workflow',
        verbose_name=_('工作流程'),
        blank=True, null=True,
        on_delete=models.PROTECT,
        db_constraint=False,
        limit_choices_to={'order_relation_config': '10'},
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
    rstatus = StateField(
        verbose_name=_('状态'),
        blank=True, null=True,
        on_delete=models.PROTECT,
        db_constraint=False,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('申请者'),
        blank=True, null=True,
        on_delete=models.CASCADE,
        db_constraint=False,
    )

    def __str__(self):
        return f'{self.code} - {self.title}'

    class Meta:
        verbose_name = _('工单')
        verbose_name_plural = _('工单')
