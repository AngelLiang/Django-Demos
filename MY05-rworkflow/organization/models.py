from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class OrgUnit(models.Model):
    """部门单元"""

    name = models.CharField(_('名称'), max_length=80)

    parent = models.ForeignKey(
        'self',
        verbose_name='上级部门',
        on_delete=models.CASCADE,
        null=True, blank=True,
        db_constraint=False,
        related_name='children',
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('部门单元')
        verbose_name_plural = _('部门单元')
