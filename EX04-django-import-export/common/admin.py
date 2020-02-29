"""
https://django-import-export.readthedocs.io/en/latest/getting_started.html#admin-integration
"""
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
# action
from import_export.admin import ImportExportActionModelAdmin
from import_export.admin import ExportActionMixin

from .models import Book, Category, Author

# Register your models here.


class BookAdmin(ImportExportModelAdmin):
    pass


class CategoryAdmin(ExportActionMixin, admin.ModelAdmin):
    pass


class AuthorAdmin(ImportExportActionModelAdmin):
    pass


admin.site.register(Book, BookAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Author, AuthorAdmin)
