from django.contrib import admin

from djtoolbox.import_export_utils.mixins import ImportExportMixin
from ..resources import DictionaryItemResource
from import_export.formats.base_formats import XLSX

class DictionaryItemAdmin(ImportExportMixin,
                          admin.ModelAdmin):
    search_fields = ('code', 'label')
    sortable_by = ()
    list_display = ('master', 'code', 'label', )
    list_filter = ('master',)

    resource_class = DictionaryItemResource
    formats = (XLSX,)
