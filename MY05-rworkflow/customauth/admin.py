from django.contrib import admin
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Role


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('code', 'username', 'password')}),
        # 个人信息
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email',)}),
        (_('所属组织机构'), {'fields': (
            ('orgunit', ),
        )}),
        # 权限
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'), }),
        # 重要日期
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(Role)
admin.site.register(User, UserAdmin)
