from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=255)


class Post(models.Model):
    title = models.CharField(max_length=255)
    summery = models.TextField()
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE
    )
