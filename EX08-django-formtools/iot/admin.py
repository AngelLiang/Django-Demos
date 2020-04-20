from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.Category)
admin.site.register(models.Device)
admin.site.register(models.Attribute)
admin.site.register(models.Value)
