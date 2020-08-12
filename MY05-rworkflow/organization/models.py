from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class OrgUnit(models.Model):
    """部门单元"""

    name = models.CharField(_('名称'), max_length=80)

    class Meta:
        verbose_name = _('部门单元')
        verbose_name_plural = _('部门单元')
