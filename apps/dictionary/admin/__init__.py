from django.contrib import admin

from .dictionary import DictionaryAdmin

from .. import models

admin.site.register(models.Dictionary, DictionaryAdmin)
