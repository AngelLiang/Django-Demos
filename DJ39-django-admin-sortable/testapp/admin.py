from django.contrib import admin

from adminsortable.admin import NonSortableParentAdmin, SortableStackedInline

from .models import Category, Project


class ProjectInline(SortableStackedInline):
    model = Project
    extra = 1


class CategoryAdmin(NonSortableParentAdmin):
    inlines = [ProjectInline]


admin.site.register(Category, CategoryAdmin)
