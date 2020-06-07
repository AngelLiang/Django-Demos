from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from mptt.admin import MPTTModelAdmin

from customauth import models
# from .user_inline import UserInline


class RoleAdmin(MPTTModelAdmin):
    list_display = ['name', 'code', 'created_at']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']

    # inlines = [
    #     UserInline,
    # ]

    fieldsets = (
        (None, {'fields':
                ('name', 'code', 'parent',
                 'description',
                 'created_at', 'updated_at', 'created_by', 'updated_by',
                 )}
         ),
    )

    add_fieldsets = (
        (None, {'fields': ('name', 'code', 'parent', 'description',)}),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def save_model(self, request, obj, form, change):
        """override"""
        obj.updated_by = request.user
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
