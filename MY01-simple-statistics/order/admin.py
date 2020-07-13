import calendar
from django.contrib import admin

from django.contrib.admin.views.main import ChangeList
from django.db.models import (
    Count, Sum, Min, Max, Avg,
    DateTimeField, DateField
)
from django.db.models.functions import (
    Trunc, TruncYear, TruncDay,
    Extract,
    ExtractYear, ExtractMonth, ExtractDay, ExtractHour,
    ExtractQuarter
)

from . import models
from .reportutils import (
    gen_changelist_title, get_chart_data, get_chart_title
)


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
    list_display = ('order_date', 'title', 'amount', 'customer', 'created_at')
    # list_filter = ('customer',)
    search_fields = ('title',)

    readonly_fields = ('amount',)
    inlines = (OrderItemInline,)
    ordering = ('created_at',)
    date_hierarchy = 'created_at'

    chart_show = True

    class Media:
        css = {
            'all': ('css/admin/css/barchart.css',)
        }

    def get_changelist_instance(self, request):
        cl = super().get_changelist_instance(request)
        cl.title = gen_changelist_title(request, self.date_hierarchy, self.opts.verbose_name)
        return cl

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        # self.get_queryset would return the base queryset. ChangeList
        # apply the filters from the request so this is the only way to
        # get the filtered queryset.

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            # See issue #172.
            # When an invalid filter is used django will redirect. In this
            # case the response is an http redirect response and so it has
            # no context_data.
            return response

        response.context_data['chart_title'] = get_chart_title(request, self.date_hierarchy)
        response.context_data['chart_data'] = get_chart_data(request, qs, self.date_hierarchy)

        return response


admin.site.register(models.Customer, CustomerAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Order, OrderAdmin)
