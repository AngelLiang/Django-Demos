from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
# Register your models here.

from .models import Post, Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)


class PostAdmin(ImportExportModelAdmin):
    list_display = (
        'title', 'slug', 'user', 'is_delete',
        'money', 'price',
        'create_date', 'create_time', 'update_datetime',
    )
    list_filter = ['is_delete']
    search_fields = ['title']


admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
