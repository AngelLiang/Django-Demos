from django.contrib import admin

from . import models


class TempUserViewAdmin(admin.ModelAdmin):
    """数据库视图只可查看不可编辑"""

    def has_view_permission(self, request, obj=None):
        """必须覆写否则可能显示不出来
        https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.has_view_permission
        """
        return True

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(models.TempUser, TempUserViewAdmin)
