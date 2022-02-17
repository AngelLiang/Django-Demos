from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import get_user_model
User = get_user_model()


class Dictionary(models.Model):
    code = models.CharField(_("编码"), max_length=16, unique=True)
    name = models.CharField(_("名称"), max_length=128, blank=True, default="")
    is_locked = models.BooleanField(_("锁定"), default=False)
    in_use = models.BooleanField(_("使用中"), default=False)
    locked_at = models.DateTimeField(_("锁定时间"), null=True, blank=True)
    # locked_by = models.ForeignKey(
    #     User, verbose_name=_("锁定人"),
    #     blank=True, null=True,
    #     on_delete=models.CASCADE,
    #     db_constraint=False,
    # )

    class Meta:
        verbose_name = _('字典管理')
        verbose_name_plural = _('字典管理')
