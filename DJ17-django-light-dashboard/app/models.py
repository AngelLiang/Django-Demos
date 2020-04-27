from decimal import Decimal

from django.db import models


class Device(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class Sale(models.Model):
    created = models.DateTimeField()
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
    )
    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
    )
    price = models.DecimalField(
        max_digits=8, decimal_places=2,
        blank=True, default=Decimal('0.0')
    )

    def __str__(self):
        return '[{}] {:%Y-%m-%d}'.format(self.id, self.created)


class SaleSummary(Sale):
    class Meta:
        proxy = True
        verbose_name = 'Sale Summary'
        verbose_name_plural = 'Sales Summary'
