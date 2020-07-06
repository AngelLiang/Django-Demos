from django.contrib import admin

from django.db.models import Sum, Avg, Count, Min, Max
from admin_report.mixins import ChartReportAdmin
from import_export import resources
from import_export.admin import ExportMixin
from import_export import fields
from django.utils import formats

from .models import Order, OrderItem, OrderProxy, Product, ProductProxy


class AdminNoAddPermissionMixin(object):
    def has_add_permission(self, request):
        return False


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class OrderAdmin(admin.ModelAdmin):
        # search_fields = ('nome', 'email', 'cpf', 'rg')
    list_display = ('data', 'payment_type', 'email',
                    'delivered', 'total_value', 'gender')
    list_filter = ('data', 'payment_type')
    inlines = [OrderItemInline]


    # date_hierarchy = 'data'
    # exclude = ('grupo_tributacao',)
admin.site.register(Order, OrderAdmin)


class ReportOrderAdmin(ExportMixin, AdminNoAddPermissionMixin, ChartReportAdmin):
    list_filter = ['payment_type', 'email', 'delivered']
    list_display = ('data', 'payment_type', 'email',
                    'delivered', 'total_value', 'gender')

    # group_by = "gender"

    report_aggregates = (
        ('total_value', Sum, "<b>Total vendido</b>"),
        ('total_value', Avg, "<b>Valor médio</b>"),
        ('total_value', Count, "<b>Número de pedidos</b>"),
    )


admin.site.register(OrderProxy, ReportOrderAdmin)


class ReportOrderItemsResource(resources.ModelResource):
    orderitem__value__avg = fields.Field(
        attribute="orderitem__value__avg", column_name="valor médio do produto")
    orderitem__value__max = fields.Field(
        attribute="orderitem__value__max", column_name="maior valor de venda")
    orderitem__value__min = fields.Field(
        attribute="orderitem__value__min", column_name="menor valor de venda")
    orderitem__quantity__sum = fields.Field(
        attribute="orderitem__quantity__sum", column_name="total de itens vendidos")
    orderitem__total__sum = fields.Field(
        attribute="orderitem__total__sum", column_name="valor total vendido")

    class Meta:
        model = ProductProxy
        fields = ('name', 'orderitem__value__avg', 'orderitem__value__max',
                  'orderitem__value__min', 'orderitem__quantity__sum', 'orderitem__total__sum',)
        export_order = fields

    def dehydrate_orderitem__value__avg(self, obj):
        return u"R$ {0}".format(formats.number_format(obj.orderitem__value__avg, 2))

    def dehydrate_orderitem__value__max(self, obj):
        return formats.number_format(obj.orderitem__value__max, 2)

    def dehydrate_orderitem__value__min(self, obj):
        return formats.number_format(obj.orderitem__value__min, 2)

    def dehydrate_orderitem__quantity__sum(self, obj):
        return formats.number_format(obj.orderitem__quantity__sum, 2)

    def dehydrate_orderitem__total__sum(self, obj):
        return formats.number_format(obj.orderitem__total__sum, 2)


class ReportOrderItemsAdmin(ExportMixin, AdminNoAddPermissionMixin, ChartReportAdmin):
    resource_class = ReportOrderItemsResource
    list_filter = ['name', 'orderitem__order__payment_type', ]
    list_display = ('name', 'valor_atual', 'orderitem__value__avg', 'orderitem__value__max',
                    'orderitem__value__min', 'orderitem__quantity__sum', 'orderitem__total__sum',)

    def valor_atual(self, obj):
        return obj.value
    valor_atual.short_description = 'valor atual do produto'
    valor_atual.admin_order_field = 'value'
    # valor_atual.allow_tags = True

    report_annotates = (
        ("orderitem__quantity", Sum, "销售总额"),
        ("orderitem__total", Sum, "销售数量"),
        # ("orderitem__total", Count, "count total vendido"),
        ("orderitem__value", Avg, "平均销售价"),
        ("orderitem__value", Max, "最高销售价"),
        ("orderitem__value", Min, "最低销售价"),
        # ("orderitem__valor_sem_desconto", Min, "menor valor do produto"),
    )

    report_aggregates = (
        ('orderitem__total__sum', Sum, "<b>Total: R$ %value</b>"),
        ('orderitem__quantity', Sum, "total de itens vendidos"),
    )


admin.site.register(ProductProxy, ReportOrderItemsAdmin)


class ProductAdmin(admin.ModelAdmin):
    # search_fields = ('nome', 'email', 'cpf', 'rg')
    list_display = ('name', 'value')


    # date_hierarchy = 'data'
    # exclude = ('grupo_tributacao',)
admin.site.register(Product, ProductAdmin)
