from django.db import models
from django.utils.translation import ugettext_lazy as _


class DictionarytItem(models.Model):
    master = models.ForeignKey(
        'Dictionary',
        verbose_name=_("字典管理"),
        on_delete=models.CASCADE,
        db_constraint=False
    )
    code = models.CharField(_("编码"), max_length=16)
    label = models.CharField(_("标签"), max_length=128, blank=True, default="")

    class Meta:
        verbose_name = _('字典明细')
        verbose_name_plural = _('字典明细')
        # unique_together = ('master', 'key')
