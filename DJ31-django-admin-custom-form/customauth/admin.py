from django.contrib import admin

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    pass


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
