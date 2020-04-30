from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from . import models


class UserAdmin(BaseUserAdmin):
    # can_delete = False
    list_display = (
        'username', 'email',
        'first_name', 'last_name', 'organization',
        'is_staff', 'is_active',
    )
    readonly_fields = ('last_login', 'date_joined',)
    list_filter = (
        'organization',
        'is_staff', 'is_superuser',
        'is_active', 'groups',
    )

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        # 在个人信息后面添加 organization 字段
        (_('Personal info'), {
         'fields': ('first_name', 'last_name', 'email', 'organization')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
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


# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
# admin.site.unregister(Group)
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Organization)
