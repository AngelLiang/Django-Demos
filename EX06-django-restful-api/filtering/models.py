from django.db import models
from django.conf import settings

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, null=True, blank=True)
    in_stock = models.BooleanField(default=False)


class Purchase(models.Model):
    name = models.CharField(max_length=100)

    purchaser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True, blank=True,
    )
