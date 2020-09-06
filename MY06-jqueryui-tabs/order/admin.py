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


class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'order_date', 'title', 'amount')
    readonly_fields = ('amount',)
    inlines = (OrderItemInline,)
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'order_date',
                'amount',
            ),
        }),
        ('客户', {
            'fields': (
                'customer',
            ),
        }),
    )

    # def save_model(self, request, obj, form, change):
    #     super().save_model(request, obj, form, change)
    #     obj.update_amount()

    class Media:
        js = (
            'jquery-ui-1.12.1/jquery-ui.min.js',
        )
        css = {
            'all': ('jquery-ui-1.12.1/jquery-ui.min.css',)
        }


admin.site.register(models.Customer, CustomerAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Order, OrderAdmin)
