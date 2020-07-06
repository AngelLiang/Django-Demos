from django.db import models

from django.utils.translation import ugettext_lazy as _


class Country(models.Model):
    name = models.CharField('名称', max_length=16)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('国家')
        verbose_name_plural = _('国家')


class Province(models.Model):
    name = models.CharField('名称', max_length=16)

    country = models.ForeignKey(
        Country,
        verbose_name=_('国家'),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('省份')
        verbose_name_plural = _('省份')


class Address(models.Model):
    country = models.ForeignKey(
        Country,
        verbose_name=_('国家'),
        on_delete=models.CASCADE,
    )

    province = models.ForeignKey(
        Province,
        verbose_name=_('省份'),
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _('地址')
        verbose_name_plural = _('地址')
