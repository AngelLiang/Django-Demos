import json
from django.contrib import admin
from django.conf.urls import url
from django.http import HttpResponse


from . import models


class CustomerAdmin(admin.ModelAdmin):
    pass


class ProductAdmin(admin.ModelAdmin):
    search_fields = ('name',)

    def get_urls(self):
        urls = super().get_urls()
        return [
            url(r'(?P<obj_id>\d+)/price/', self.get_price_json, name='get_price_json'),
        ] + urls

    def get_price_json(self, request, obj_id):
        """获取单价"""
        obj = self.get_object(request, obj_id)
        if obj is None:
            # opts = self.opts
            # return self._get_obj_does_not_exist_redirect(request, opts, obj_id)
            return HttpResponse(json.dumps({}), content_type="application/json")
        result = {'price': str(obj.price)}
        return HttpResponse(json.dumps(result), content_type="application/json")


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    extra = 1
    fields = ('product', 'quantity', 'price', 'amount',)
    readonly_fields = ('amount',)
    # autocomplete_fields = ('product',)


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
