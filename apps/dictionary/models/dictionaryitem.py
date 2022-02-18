from django.db import models
from django.utils.translation import ugettext_lazy as _


class DictionaryItem(models.Model):
    master = models.ForeignKey(
        'Dictionary',
        verbose_name=_("字典管理"),
        on_delete=models.CASCADE,
        db_constraint=False,
        related_name='items',
    )
    code = models.CharField(_("编码"), max_length=40)
    label = models.CharField(_("标签"), max_length=128, blank=True, default="")

    class Meta:
        verbose_name = _('字典明细')
        verbose_name_plural = _('字典明细')
        # unique_together = ('master', 'key')
        default_permissions = ()
        permissions = (
            # 功能权限
            ('add_dictionaryitem', _('允许添加字典明细')),
            ('view_dictionaryitem', _('允许查看字典明细')),
            ('change_dictionaryitem', _('允许修改字典明细')),
            ('delete_dictionaryitem', _('允许删除字典明细')),
            ('import_dictionaryitem', _('允许导入字典明细')),
            ('export_dictionaryitem', _('允许导出字典明细')),
        )

    def __str__(self):
        return self.code
