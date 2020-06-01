# from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.utils.translation import gettext, gettext_lazy as _


class GroupAdmin(BaseGroupAdmin):
    pass
