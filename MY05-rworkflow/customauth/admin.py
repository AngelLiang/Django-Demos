from django.contrib import admin
from django.utils.translation import gettext, gettext_lazy as _

from .models import Role


admin.site.register(Role)
