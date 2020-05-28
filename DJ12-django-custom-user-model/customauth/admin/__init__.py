from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin

from .user import UserAdmin
from .role import RoleAdmin
from .organization import OrganizationAdmin
from customauth import models


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Role, RoleAdmin)
admin.site.register(models.Organization, OrganizationAdmin)
# admin.site.unregister(Group)
# admin.site.register(Group)
