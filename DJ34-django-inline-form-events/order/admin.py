from django.contrib import admin

from . import models


class CustomerAdmin(admin.ModelAdmin):
    pass


class ProductAdmin(admin.ModelAdmin):
    pass


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    extra = 1
    fields = ('product', 'quantity', 'price', 'amount',)
    readonly_fields = ('amount',)
    max_num = 4


class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'order_date', 'title', 'amount')
    readonly_fields = ('amount',)
    inlines = (OrderItemInline,)

    # def save_model(self, request, obj, form, change):
    #     super().save_model(request, obj, form, change)
    #     obj.update_amount()


admin.site.register(models.Customer, CustomerAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Order, OrderAdmin)
