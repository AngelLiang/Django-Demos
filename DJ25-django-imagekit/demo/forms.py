from django import forms
from django.forms import models
from imagekit.forms import ProcessedImageField
from imagekit.processors import ResizeToFill

from .models import Photo


class PhotoForm(models.ModelForm):
    # avatar_thumbnail = ProcessedImageField(
    #     spec_id='demo:profile:avatar_thumbnail',
    #     processors=[ResizeToFill(100, 50)],
    #     format='JPEG',
    #     options={'quality': 60})

    class Meta:
        model = Photo
        fields = '__all__'
