from django.contrib import admin
from advanced_filters.admin import AdminAdvancedFiltersMixin

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


class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'order_date', 'title', 'amount')
    readonly_fields = ('amount',)
    list_filter = ('order_date', )
    inlines = (OrderItemInline,)

    # def save_model(self, request, obj, form, change):
    #     super().save_model(request, obj, form, change)
    #     obj.update_amount()


class OrderAdvancedFilterAdmin(AdminAdvancedFiltersMixin, OrderAdmin):
    list_filter = ('order_date', )   # simple list filters

    # specify which fields can be selected in the advanced filter
    # creation form
    advanced_filter_fields = (
        'title',
        'order_date',

        # even use related fields as lookup fields
        'customer__name',
    )


admin.site.register(models.Customer, CustomerAdmin)
admin.site.register(models.Product, ProductAdmin)
# admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.Order, OrderAdvancedFilterAdmin)
