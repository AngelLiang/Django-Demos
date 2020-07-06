from django.contrib import admin

from . import models


class ProductAdmin(admin.ModelAdmin):
    pass


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_date', 'title', 'amount')
    inlines = (OrderItemInline,)

    # readonly_fields = ('amount',)


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Order, OrderAdmin)
