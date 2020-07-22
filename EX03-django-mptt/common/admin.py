from django.contrib import admin

from mptt.admin import MPTTModelAdmin
# from mptt.admin import DraggableMPTTAdmin
# from mptt.admin import TreeRelatedFieldListFilter

from .models import Genre


class MPTTAdmin(MPTTModelAdmin):
    model = Genre
    list_display = ('name', 'parent')
    # list_filter = (
    #     ('my_related_model', TreeRelatedFieldListFilter),
    # )


admin.site.register(Genre, MPTTAdmin)
