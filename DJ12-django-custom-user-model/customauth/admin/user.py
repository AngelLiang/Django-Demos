from django.conf import settings
from django.contrib import admin
# from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from mptt.admin import MPTTModelAdmin

from customauth import models


class UserAdmin(BaseUserAdmin):
    # can_delete = False
    list_display = (
        'username', 'email',
        'get_full_name',
        'organization',
        'is_staff', 'is_active',
    )
    readonly_fields = ['last_login', 'date_joined', ]
    list_filter = (
        'organization',
        'is_staff', 'is_superuser',
        'is_active', 'groups',
        'roles',
    )
    # 添加 roles
    filter_horizontal = ('groups', 'user_permissions', 'roles',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        # 个人信息
        # 在个人信息后面添加 phone, organization 字段
        (_('Personal info'), {
         'fields': ('first_name', 'last_name', 'email', 'phone', 'organization')}),
        #  角色
        ('角色', {'fields': ('roles',)}),
        # 权限
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        # 重要日期
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            # 添加 organization 字段
            'fields': ('username', 'password1', 'password2', 'is_staff', 'organization'),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = self.readonly_fields
        user = request.user
        if obj and not user.is_superuser:
            readonly_fields.append('username')
        return readonly_fields

    def has_delete_permission(self, request, obj=None):
        return False
