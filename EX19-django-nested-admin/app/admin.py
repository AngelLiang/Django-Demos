from django.contrib import admin
import nested_admin

from .models import LevelOne, LevelThree, LevelTwo, TopLevel


class LevelThreeInline(nested_admin.NestedStackedInline):
    model = LevelThree
    extra = 1
    fk_name = 'level'


class LevelTwoInline(nested_admin.NestedStackedInline):
    model = LevelTwo
    extra = 1
    # sortable_field_name = "position"
    fk_name = 'level'
    inlines = [LevelThreeInline]


class LevelOneInline(nested_admin.NestedStackedInline):
    model = LevelOne
    extra = 1
    # sortable_field_name = "position"
    fk_name = 'level'
    inlines = [LevelTwoInline]


class TopLevelAdmin(nested_admin.NestedModelAdmin):
    model = TopLevel
    inlines = [LevelOneInline]


admin.site.register(TopLevel, TopLevelAdmin)
