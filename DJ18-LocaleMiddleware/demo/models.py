from django.db import models
from django.utils.translation import gettext_lazy as _


class Demo(models.Model):
    name = models.CharField(_('name'), max_length=80)
