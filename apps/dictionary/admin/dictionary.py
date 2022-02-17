from django.contrib import admin

from djtoolbox.import_export_utils.mixins import ImportExportMixin
from .dictionaryiteminline import DictionarytItemInline


class DictionaryAdmin(ImportExportMixin,
                      admin.ModelAdmin):
    sortable_by = ()
    list_display = ('code', 'name', 'is_locked')
    list_editable = ('is_locked',)
    inlines = (DictionarytItemInline,)
    readonly_fields = ('locked_at',)
