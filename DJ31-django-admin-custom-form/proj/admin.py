from django.contrib import admin

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    change_form_template = 'admin/auth/user/change_form.html'


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
