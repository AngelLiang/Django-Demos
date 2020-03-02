from django.contrib import admin

# Register your models here.
from .models import Post


# class PostAdmin(admin.ModelAdmin):
#     prepopulated_fields = {"slug": ("title",)}
#     list_display = ('title', 'slug', 'created_at')
#     search_fields = ('title', 'content')
#     ordering = ('-created_at',)
#     date_hierarchy = 'created_at'


# admin.site.register(Post, PostAdmin)


from guardian.admin import GuardedModelAdmin


class PostAdmin(GuardedModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'slug', 'created_at')
    search_fields = ('title', 'content')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'


admin.site.register(Post, PostAdmin)
