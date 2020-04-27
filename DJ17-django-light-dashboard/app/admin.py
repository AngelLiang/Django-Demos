from django.contrib import admin
from django.db.models import Count, Sum, Min, Max, DateTimeField
from django.db.models.functions import Trunc

from . import models


def get_next_in_date_hierarchy(request, date_hierarchy):
    if date_hierarchy + '__day' in request.GET:
        return 'hour'
    if date_hierarchy + '__month' in request.GET:
        return 'day'
    if date_hierarchy + '__year' in request.GET:
        return 'week'
    return 'month'


@admin.register(models.Device)
class DeviceModelAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Category)
class CategoryModelAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Sale)
class SaleModelAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'price']
    list_filter = (
        'device',
    )


@admin.register(models.SaleSummary)
class SaleSummaryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/dashboard/sales_change_list.html'
    actions = None
    date_hierarchy = 'created'
    # Prevent additional queries for pagination.
    show_full_result_count = False

    list_filter = (
        'device',
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_module_permission(self, request):
        return True

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

        # List view

        # 需要统计的列
        metrics = {
            'total': Count('id'),
            'total_price': Sum('price'),
        }

        # 按分类统计
        # total_price 正序
        response.context_data['summary'] = list(
            qs.values('category__name').annotate(
                **metrics).order_by('total_price')
        )

        # List view summary
        response.context_data['summary_total'] = dict(qs.aggregate(**metrics))

        # Chart
        period = get_next_in_date_hierarchy(request, self.date_hierarchy)
        response.context_data['period'] = period
        summary_over_time = qs.annotate(
            period=Trunc('created', 'day', output_field=DateTimeField()),
        ).values('period').annotate(total=Sum('price')).order_by('period')

        summary_range = summary_over_time.aggregate(
            low=Min('total'),
            high=Max('total'),
        )
        high = summary_range.get('high', 0)
        low = summary_range.get('low', 0)

        response.context_data['summary_over_time'] = [{
            'period': x['period'],
            'total': x['total'] or 0,
            'pct':
            ((x['total'] or 0) - low) / (high - low) * 100
            if high > low else 0,
        } for x in summary_over_time]

        return response
