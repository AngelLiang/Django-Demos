from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    orgunit = models.ForeignKey(
        'organization.OrgUnit',
        verbose_name=_('所属单元部门'),
        on_delete=models.PROTECT,
        null=True, blank=True,
        db_constraint=False,
        related_name='+',
    )

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        default_permissions = ('view', 'add', 'change')


class Role(models.Model):

    name = models.CharField(_('角色名称'), max_length=80)

    # 用户：多对多关系
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('用户'),
        blank=True,
        db_constraint=False,
        related_name='roles',
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('角色')
        verbose_name_plural = _('角色')
