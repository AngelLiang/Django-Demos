from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from mptt.admin import MPTTModelAdmin

from customauth import models


class RoleAdmin(MPTTModelAdmin):
    list_display = ['name', 'code', 'created_at']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']

    # inlines = [
    #     UserInline,
    # ]

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
