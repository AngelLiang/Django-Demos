from django.contrib import admin

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
    list_display = ('__str__', 'order_date', 'title', 'amount', 'created_at')
    readonly_fields = ('amount',)
    inlines = (OrderItemInline,)
    list_filter = ('created_at',)

    ordering = ('created_at',)
    date_hierarchy = 'created_at'

    class Media:
        css = {
            'all': ('css/admin/css/barchart.css',)
        }

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

        def get_date_hierarchy(request, date_hierarchy):
            if 'created_at__gte' in request.GET:
                return None
            # 不能调动以下判断顺序，因为要从小到大判断
            if date_hierarchy + '__day' in request.GET:
                return 'hour'
            if date_hierarchy + '__month' in request.GET:
                return 'day'
            if date_hierarchy + '__year' in request.GET:
                return 'month'
            return 'year'

        extract_field = self.date_hierarchy
        date_hierarchy = get_date_hierarchy(request, self.date_hierarchy)

        # print(date_hierarchy)
        if date_hierarchy == 'year':
            # 按年份统计数量
            show_chart = True
            title = '年份统计图'
            annotate_options = {'year': ExtractYear(extract_field)}
            values_args = ('year',)
            order_by_args = values_args
        elif date_hierarchy == 'month':
            # 按年月统计数量
            show_chart = True
            title = '月份统计图'
            annotate_options = {
                'year': ExtractYear(extract_field),
                'month': ExtractMonth(extract_field)
            }
            values_args = ('year', 'month')
            order_by_args = values_args
        elif date_hierarchy == 'day':
            # 按年月日统计数量
            show_chart = True
            title = '日期统计图'
            annotate_options = {
                'year': ExtractYear(extract_field),
                'month': ExtractMonth(extract_field),
                'day': ExtractDay(extract_field),
            }
            values_args = ('year', 'month', 'day')
            order_by_args = values_args
        elif date_hierarchy == 'hour':
            # 按年月日时统计数量
            show_chart = True
            title = '小时统计图'
            annotate_options = {
                'year': ExtractYear(extract_field),
                'month': ExtractMonth(extract_field),
                'day': ExtractDay(extract_field),
                'hour': ExtractHour(extract_field),
            }
            values_args = ('year', 'month', 'day', 'hour')
            order_by_args = values_args
        else:
            # 按年份统计数量
            show_chart = False
            title = ''
            annotate_options = {}
            values_args = ()
            order_by_args = values_args
        # 统计数量

        total_every_period = qs.annotate(
            **annotate_options
        ).values(*values_args).order_by(*order_by_args).annotate(total=Count('id'))

        # total_every_period = total_every_period.annotate(
        #     period=TruncDay('order_date', output_field=DateField())
        # )
        # print(total_every_period)

        # 获取最小值和最大值
        total_range = total_every_period.aggregate(low=Min('total'), high=Max('total'))
        # print(total_range)
        high = total_range.get('high', 0)
        low = total_range.get('low', 0)

        summary_over_time = []
        for x in total_every_period:
            year = x.get('year')
            month = x.get('month')
            day = x.get('day')
            hour = x.get('hour')
            period_label = ''
            if year:
                period_label += f'{year}'
            if month:
                period_label += f'-{month}'
            if day:
                period_label += f'-{day}'
            if hour:
                period_label += f' {hour}:00'

            total = x.get('total') or 0
            temp = {
                'period_label': period_label,
                'period': period_label,
                'total': total,
                'pct': round((total / high) * 100, 2) if high else 0,
            }
            summary_over_time.append(temp)

        # print(summary_over_time)
        response.context_data['summary_over_time'] = summary_over_time
        response.context_data['show_chart'] = show_chart
        response.context_data['chart_title'] = title

        return response


admin.site.register(models.Customer, CustomerAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Order, OrderAdmin)
