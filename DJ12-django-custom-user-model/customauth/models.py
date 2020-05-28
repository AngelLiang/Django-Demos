from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from mptt.models import MPTTModel, TreeForeignKey


class User(AbstractUser):
    phone = models.CharField(
        '手机号码',
        max_length=16,
        null=True, blank=True,
    )
    organization = models.ForeignKey(
        'Organization',
        verbose_name='所属组织',
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
    roles = models.ManyToManyField(
        'Role',
        verbose_name='角色',
        blank=True,
        db_constraint=False,
        related_name='menbers',
    )

    # def __str__(self):
    #     return self.name

    # class Meta:
    #     verbose_name = '帐号'
    #     verbose_name_plural = verbose_name


class Role(MPTTModel, models.Model):
    name = models.CharField('角色名称', max_length=80)
    code = models.CharField(
        '角色编码', max_length=32,
        null=True, blank=True,
        db_index=True, unique=True
    )
    parent = TreeForeignKey(
        'self', on_delete=models.CASCADE,
        verbose_name='父级角色',
        null=True, blank=True,
        related_name='children'
    )

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='创建人',
        on_delete=models.CASCADE,
        db_constraint=False,
        related_name='+',
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='最后修改人',
        on_delete=models.CASCADE,
        db_constraint=False,
        related_name='+',
    )
    description = models.TextField('描述', default='')

    def get_menbers(self):
        return self.menbers.all()
    get_menbers.description = '主要成员'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '角色'
        verbose_name_plural = verbose_name


class Organization(MPTTModel, models.Model):
    name = models.CharField('组织名称', max_length=80)
    code = models.CharField(
        '组织编码', max_length=32,
        null=True, blank=True,
        db_index=True, unique=True
    )
    parent = TreeForeignKey(
        'self', on_delete=models.CASCADE,
        verbose_name='父级组织',
        null=True, blank=True,
        related_name='children'
    )
    leader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='负责人',
        on_delete=models.CASCADE,
        db_constraint=False,
        related_name='+',
    )

    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='创建人',
        on_delete=models.CASCADE,
        db_constraint=False,
        related_name='+',
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='最后修改人',
        on_delete=models.CASCADE,
        db_constraint=False,
        related_name='+',
    )

    description = models.TextField('描述', default='')

    def get_main_menbers(self):
        return self.main_menbers.all()
    get_main_menbers.description = '主要成员'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '组织'
        verbose_name_plural = verbose_name

    # class MPTTMeta:
    #     order_insertion_by = ['name']
