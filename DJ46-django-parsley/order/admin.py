from django.contrib import admin
from parsley.mixins import ParsleyAdminMixin

from . import models
from .form import OrderForm


class CustomerAdmin(ParsleyAdminMixin, admin.ModelAdmin):

    class Media:
        js = (
            "//code.jquery.com/jquery-latest.min.js",
            "parsley/js/parsley.min.js",
            "parsley/js/parsley.django-admin.js"
        )


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
    form = OrderForm

    # def save_model(self, request, obj, form, change):
    #     super().save_model(request, obj, form, change)
    #     obj.update_amount()


admin.site.register(models.Customer, CustomerAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Order, OrderAdmin)
