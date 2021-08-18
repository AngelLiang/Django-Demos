from django.contrib import admin

from . import models
from .softdeletion import SoftDeletionAdminMixin


class CustomerAdmin(admin.ModelAdmin):
    pass


class ProductAdmin(admin.ModelAdmin):
    pass


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    extra = 1
    fields = ('product', 'quantity', 'price', 'amount',)
    readonly_fields = ('amount',)


class OrderAdmin(SoftDeletionAdminMixin, admin.ModelAdmin):
    list_display = ('__str__', 'order_date', 'title', 'amount', 'is_deleted')
    readonly_fields = ('amount',)
    inlines = (OrderItemInline,)

    # def save_model(self, request, obj, form, change):
    #     super().save_model(request, obj, form, change)
    #     obj.update_amount()


class OrderItemAdmin(SoftDeletionAdminMixin, admin.ModelAdmin):
    list_display = ('__str__', 'is_deleted')


admin.site.register(models.Customer, CustomerAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderItem, OrderItemAdmin)
