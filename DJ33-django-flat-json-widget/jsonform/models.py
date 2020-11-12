from django.db import models


class JsonDocument(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
