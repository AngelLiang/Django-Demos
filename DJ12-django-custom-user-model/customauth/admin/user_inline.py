from django.contrib import admin

from . import models


class UserInline(admin.TabularInline):
    # model = settings.AUTH_USER_MODEL
    model = models.User
    can_delete = False
    fields = ['username', 'email', 'is_active', 'date_joined']

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    # def has_delete_permission(self, request, obj=None):
    #     return False
