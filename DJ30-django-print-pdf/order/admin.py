import weasyprint

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string

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

    # def save_model(self, request, obj, form, change):
    #     super().save_model(request, obj, form, change)
    #     obj.update_amount()

    def get_urls(self):
        urls = super().get_urls()
        return [
            path(r'<int:obj_id>/print', self.print_pdf,
                 name=f'{self.opts.app_label}_{self.opts.model_name}_print'),
        ] + urls

    def print_pdf(self, request, obj_id):
        obj = self.get_object(request, obj_id)
        html = render_to_string('admin/order/order/pdf.html', {'order': obj})
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'filename={obj}.pdf"'
        weasyprint.HTML(string=html).write_pdf(
            response,
            stylesheets=[weasyprint.CSS(
                settings.STATIC_ROOT + 'css/pdf.css')])
        return response


admin.site.register(models.Customer, CustomerAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Order, OrderAdmin)
