from django.contrib import admin
from django.conf import settings
from django.contrib.auth.models import Group
# from django.contrib.auth.admin import GroupAdmin

from .user import UserAdmin
from .role import RoleAdmin
from .organization import OrganizationAdmin
from .group import GroupAdmin

from customauth import models
from django.contrib.auth import get_user_model
User = get_user_model()

# admin.site.register(models.User, UserAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(models.Role, RoleAdmin)
admin.site.register(models.Organization, OrganizationAdmin)

admin.site.unregister(Group)
admin.site.register(models.ProxyGroup, GroupAdmin)
