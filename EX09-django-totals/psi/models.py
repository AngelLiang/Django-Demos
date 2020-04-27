from decimal import Decimal

from django.db import models


class Expense(models.Model):

    amount = models.DecimalField(
        verbose_name='支出总计',
        max_digits=8, decimal_places=2,
        blank=True, default=Decimal('0.0')
    )
    has_invoice = models.BooleanField(
        '是否有发票',
        default=False,
    )

    total = models.DecimalField(
        verbose_name='货物数量',
        max_digits=8, decimal_places=2,
        blank=True, default=Decimal('0.0')
    )
