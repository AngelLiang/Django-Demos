"""
https://django-import-export.readthedocs.io/en/latest/getting_started.html#admin-integration
"""
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Book

# Register your models here.


class BookAdmin(ImportExportModelAdmin):
    pass


admin.site.register(Book, BookAdmin)
