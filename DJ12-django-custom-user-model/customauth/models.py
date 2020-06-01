from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from .utils.soft_delete import SoftDeletableManager


class User(AbstractUser):

    name = models.CharField(
        _('名称'),
        max_length=8,
        default='', blank=True,
    )

    avatar = models.FileField(
        verbose_name=_('头像'),
        null=True, blank=True
    )

    phone = models.CharField(
        _('手机号码'),
        max_length=16,
        default='', blank=True,
    )

    # 组织：多对一关系
    # organization = models.ForeignKey(
    organization = TreeForeignKey(
        'Organization',
        verbose_name=_('所属组织'),
        null=True, blank=True,
        on_delete=models.PROTECT,
        db_constraint=False,
        related_name='main_menbers',
        limit_choices_to={'is_deleted': False},
    )
    # role = models.ForeignKey(
    #     'Role',
    #     null=True, blank=True,
    #     on_delete=models.PROTECT,
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
        limit_choices_to={'is_deleted': False},
    )

    # def __str__(self):
    #     return self.username

    # class Meta:
    #     verbose_name = _('user')
    #     verbose_name_plural = _('users')


class BaseModel(models.Model):

    class Meta:
        abstract = True

    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('创建人'),
        on_delete=models.PROTECT,
        db_constraint=False,
        related_name='+',
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('最后修改人'),
        on_delete=models.PROTECT,
        db_constraint=False,
        related_name='+',
    )
    description = models.TextField(_('描述'), default='', blank=True)

    is_deleted = models.BooleanField(
        _('已删除'), default=False, editable=False, db_index=True
    )

    # 放在这里，后台还是可以显示已经软删除的数据
    # objects = SoftDeletableManager()

    def delete(self, using=None, soft=True, *args, **kwargs):
        """
        Soft delete object(set its ``is_deleted`` field to True).
        Actually delete object if setting ``soft`` to False.
        """
        if soft:
            self.is_deleted = True
            self.save(using=using)
        else:
            return super().delete(using=using, *args, **kwargs)


class Role(MPTTModel, BaseModel):
    name = models.CharField(_('角色名称'), max_length=80)
    code = models.CharField(
        _('角色编码'), max_length=32,
        null=True, blank=True,
        db_index=True
    )
    parent = TreeForeignKey(
        'self',
        # 删除父级数据之前需要先删除子数据
        on_delete=models.PROTECT,
        verbose_name='父级角色',
        null=True, blank=True,
        related_name='children',
        # 软删除的数据不显示
        limit_choices_to={'is_deleted': False},
    )

    def get_menbers(self):
        return self.menbers.all()
    get_menbers.description = _('主要成员')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('角色')
        verbose_name_plural = _('角色')

    objects = SoftDeletableManager()


class Organization(MPTTModel, BaseModel):
    name = models.CharField(_('组织名称'), max_length=80)
    code = models.CharField(
        _('组织编码'), max_length=32,
        null=True, blank=True,
        db_index=True
    )
    parent = TreeForeignKey(
        'self',
        # 删除父级数据之前需要先删除子数据
        on_delete=models.PROTECT,
        verbose_name=_('父级组织'),
        null=True, blank=True,
        related_name='children',
        # 软删除的数据不显示
        limit_choices_to={'is_deleted': False},
    )
    leader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('负责人'),
        on_delete=models.PROTECT,
        null=True, blank=True,
        db_constraint=False,
        related_name='+',
    )

    def get_main_menbers(self):
        return self.main_menbers.all()
    get_main_menbers.description = _('主要成员')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('组织')
        verbose_name_plural = _('组织')

    # class MPTTMeta:
    #     order_insertion_by = ['name']

    objects = SoftDeletableManager()


class ProxyGroup(Group):
    """代理Group到这里的app，Group不需要软删除"""
    class Meta:
        proxy = True
        verbose_name = _('用户组')
        verbose_name_plural = _('用户组')
