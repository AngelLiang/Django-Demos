from django.db import models

# Create your models here.


class Message(models.Model):
    content = models.CharField(
        max_length=255, default='', blank=True
    )

