"""
https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#extending-the-existing-user-model
"""
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    readonly_fields = ('last_login', 'date_joined',)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
