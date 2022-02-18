from django.contrib import admin

from .dictionary import DictionaryAdmin
from .dictionaryitem import DictionaryItemAdmin


from .. import models

admin.site.register(models.Dictionary, DictionaryAdmin)
admin.site.register(models.DictionaryItem, DictionaryItemAdmin)
