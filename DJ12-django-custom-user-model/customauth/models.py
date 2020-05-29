from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey


class User(AbstractUser):

    name = models.CharField(
        _('名称'),
        max_length=8,
        null=True, blank=True,
    )

    avatar = models.FileField(
        verbose_name=_('头像'),
        null=True, blank=True
    )

    phone = models.CharField(
        _('手机号码'),
        max_length=16,
        null=True, blank=True,
    )

    # 组织：多对一关系
    organization = models.ForeignKey(
        'Organization',
        verbose_name=_('所属组织'),
        null=True, blank=True,
        on_delete=models.CASCADE,
        db_constraint=False,
        related_name='main_menbers',
    )
    # role = models.ForeignKey(
    #     'Role',
    #     null=True, blank=True,
    #     on_delete=models.CASCADE,
    #     verbose_name='角色',
    #     related_name='menbers',
    # )

    # 角色：多对多关系
    roles = models.ManyToManyField(
        'Role',
        verbose_name=_('角色'),
        blank=True,
        db_constraint=False,
        related_name='menbers',
    )

    # def __str__(self):
    #     return self.username

    # class Meta:
    #     app_label = 'auth'
    #     verbose_name = _('user')
    #     verbose_name_plural = _('users')


class ProxyUser(User):
    class Meta:
        proxy = True
        app_label = 'auth'
        verbose_name = _('user')
        verbose_name_plural = _('users')


class Role(MPTTModel, models.Model):
    name = models.CharField(_('角色名称'), max_length=80)
    code = models.CharField(
        _('角色编码'), max_length=32,
        null=True, blank=True,
        db_index=True, unique=True
    )
    parent = TreeForeignKey(
        'self', on_delete=models.CASCADE,
        verbose_name='父级角色',
        null=True, blank=True,
        related_name='children'
    )

    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('创建人'),
        on_delete=models.CASCADE,
        db_constraint=False,
        related_name='+',
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('最后修改人'),
        on_delete=models.CASCADE,
        db_constraint=False,
        related_name='+',
    )
    description = models.TextField(_('描述'), default='')

    def get_menbers(self):
        return self.menbers.all()
    get_menbers.description = _('主要成员')

    def __str__(self):
        return self.name

    class Meta:
        # app_label = 'auth'
        verbose_name = _('角色')
        verbose_name_plural = verbose_name


class ProxyRole(Role):
    class Meta:
        proxy = True
        app_label = 'auth'
        verbose_name = _('role')
        verbose_name_plural = _('roles')


class Organization(MPTTModel, models.Model):
    name = models.CharField(_('组织名称'), max_length=80)
    code = models.CharField(
        _('组织编码'), max_length=32,
        null=True, blank=True,
        db_index=True, unique=True
    )
    parent = TreeForeignKey(
        'self', on_delete=models.CASCADE,
        verbose_name=_('父级组织'),
        null=True, blank=True,
        related_name='children'
    )
    leader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('负责人'),
        on_delete=models.CASCADE,
        db_constraint=False,
        related_name='+',
    )

    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('创建人'),
        on_delete=models.CASCADE,
        db_constraint=False,
        related_name='+',
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('最后修改人'),
        on_delete=models.CASCADE,
        db_constraint=False,
        related_name='+',
    )

    description = models.TextField(_('描述'), default='')

    def get_main_menbers(self):
        return self.main_menbers.all()
    get_main_menbers.description = _('主要成员')

    def __str__(self):
        return self.name

    class Meta:
        # app_label = 'auth'
        verbose_name = _('组织')
        verbose_name_plural = verbose_name

    # class MPTTMeta:
    #     order_insertion_by = ['name']


class ProxyOrganization(Organization):
    class Meta:
        proxy = True
        app_label = 'auth'
        verbose_name = _('organization')
        verbose_name_plural = _('organizations')
