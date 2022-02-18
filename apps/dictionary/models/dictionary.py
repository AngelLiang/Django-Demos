from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import get_user_model
User = get_user_model()


class Dictionary(models.Model):
    code = models.CharField(_("编码"), max_length=40, unique=True)
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
        default_permissions = ()
        permissions = (
            # 功能权限
            ('add_dictionary', _('允许添加字典')),
            ('view_dictionary', _('允许查看字典')),
            ('change_dictionary', _('允许修改字典')),
            ('delete_dictionary', _('允许删除字典')),
            ('import_dictionary', _('允许导入字典')),
            ('export_dictionary', _('允许导出字典')),
        )

    def __str__(self):
        return self.code
