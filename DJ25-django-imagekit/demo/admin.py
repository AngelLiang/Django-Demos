from django.contrib import admin

from imagekit.admin import AdminThumbnail

from .models import Photo
from .forms import PhotoForm


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'admin_thumbnail')
    fields = (
        'avatar',
        # 'avatar_thumbnail',
    )

    admin_thumbnail = AdminThumbnail(image_field='avatar_thumbnail')
    form = PhotoForm


admin.site.register(Photo, PhotoAdmin)
