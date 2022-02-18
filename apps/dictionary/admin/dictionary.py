from django.contrib import admin

from djtoolbox.import_export_utils.mixins import ImportExportMixin
from .dictionaryiteminline import DictionaryItemInline


class DictionaryAdmin(ImportExportMixin,
                      admin.ModelAdmin):
    search_fields = ('code', 'name')
    sortable_by = ()
    list_display = ('code', 'name', 'is_locked')
    list_editable = ('is_locked',)
    inlines = (DictionaryItemInline,)
    readonly_fields = ('locked_at',)
