from django.contrib import admin

from . import models


class TempUserViewAdmin(admin.ModelAdmin):
    """数据库视图不可编辑"""

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(models.TempUser, TempUserViewAdmin)
