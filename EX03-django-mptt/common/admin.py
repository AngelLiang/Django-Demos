from django.contrib import admin

# Register your models here.

# from mptt.admin import MPTTModelAdmin
from mptt.admin import DraggableMPTTAdmin
# from mptt.admin import TreeRelatedFieldListFilter

from .models import Genre


class MPTTAdmin(DraggableMPTTAdmin):
    model = Genre
    # list_filter = (
    #     ('my_related_model', TreeRelatedFieldListFilter),
    # )


admin.site.register(
    Genre,
    MPTTAdmin,
)
