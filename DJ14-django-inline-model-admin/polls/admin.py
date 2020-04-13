from django.contrib import admin

from .models import Book, Author


class BookInline(admin.TabularInline):
    """
    admin.TabularInline: 平行的表格
    admin.StackedInline: 垂直的表格

    https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#inlinemodeladmin-options
    """
    model = Book

    readonly_fields = ['pub_date']

    def has_add_permission(self, request, obj):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


class AuthorAdmin(admin.ModelAdmin):
    inlines = [
        BookInline,
    ]


# admin.site.register(Book)
admin.site.register(Author, AuthorAdmin)
