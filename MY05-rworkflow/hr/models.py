from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class Position(models.Model):
    """岗位"""

    name = models.CharField(_('岗位名称'), max_length=80)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('岗位')
        verbose_name_plural = _('岗位')


class Employee(models.Model):
    """职员"""

    name = models.CharField(_('职员名称'), max_length=80)

    position = models.ForeignKey(
        'Position',
        null=True, blank=True,
        verbose_name=_('岗位'),
        on_delete=models.CASCADE,
        db_constraint=False,
    )

    # 关联帐号
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('关联帐号'),
        on_delete=models.PROTECT,
        db_constraint=False,
        blank=True, null=True,
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('职员')
        verbose_name_plural = _('职员')
