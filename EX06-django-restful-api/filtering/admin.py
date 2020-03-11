from django.contrib import admin

# Register your models here.
from .models import Purchase, Product

admin.site.register(Product)
admin.site.register(Purchase)
