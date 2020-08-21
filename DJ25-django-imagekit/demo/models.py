from django.db import models

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Photo(models.Model):
    avatar = models.ImageField(upload_to='avatars')
    avatar_thumbnail = ImageSpecField(
        source='avatar',
        processors=[ResizeToFill(100, 50)],
        format='JPEG',
        options={'quality': 60})
