import uuid
from decimal import Decimal

from django.db import models
from river.models.fields.state import StateField


class Product(models.Model):
    """产品"""
    name = models.CharField('名称', max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '产品'
        verbose_name_plural = verbose_name


class Order(models.Model):
    """订单"""
    sn = models.CharField('订单号', max_length=128, default=uuid.uuid4)
    created_at = models.DateTimeField(
        '创建时间', auto_now_add=True, editable=False)
    updated_at = models.DateTimeField('更新时间', auto_now=True, editable=False)

    status = StateField(verbose_name='状态', editable=False)

    def __str__(self):
        return f'{self.sn}'

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = verbose_name


class OrderItem(models.Model):
    """订单明细项"""

    product = models.ForeignKey(
        Product,
        verbose_name='产品',
        on_delete=models.CASCADE,
    )

    count = models.DecimalField(
        '数量',
        max_digits=8, decimal_places=2, blank=True, default=Decimal('0.0')
    )
    price = models.DecimalField(
        '单价',
        max_digits=8, decimal_places=2, blank=True, default=Decimal('0.0')
    )

    order = models.ForeignKey(
        Order,
        verbose_name='订单',
        on_delete=models.CASCADE,
        related_name='items',
    )

    class Meta:
        verbose_name = '订单明细项'
        verbose_name_plural = verbose_name
