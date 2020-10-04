import calendar

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


def fill_empty_date(summary_over_time, x_num, next_date_hierarchy, year, month, day):
    idx = 0
    new_summary_over_time = []
    if len(summary_over_time) != x_num:
        if next_date_hierarchy == 'month':
            for x in range(1, x_num + 1):
                try:
                    curr = summary_over_time[idx]
                    data = curr['month']
                except IndexError:
                    data = -1
                if data != x:
                    temp = {}
                    temp['total'] = 0
                    temp['pct'] = 0
                    temp['year'] = year
                    temp['month'] = x
                    temp['period_label'] = f'{year}-{x}'
                    temp['period'] = temp['period_label']
                    new_summary_over_time.append(temp)
                else:
                    new_summary_over_time.append(curr)
                    idx += 1
        elif next_date_hierarchy == 'day':
            for x in range(1, x_num + 1):
                try:
                    curr = summary_over_time[idx]
                    data = curr['day']
                except IndexError:
                    data = -1
                if data != x:
                    temp = {}
                    temp['total'] = 0
                    temp['pct'] = 0
                    temp['year'] = year
                    temp['month'] = month
                    temp['day'] = x
                    temp['period_label'] = f'{year}-{month}-{x}'
                    temp['period'] = temp['period_label']
                    new_summary_over_time.append(temp)
                else:
                    new_summary_over_time.append(curr)
                    idx += 1
        elif next_date_hierarchy == 'hour':
            for x in range(1, x_num + 1):
                try:
                    curr = summary_over_time[idx]
                    data = curr['hour']
                except IndexError:
                    data = -1
                if data != x:
                    temp = {}
                    temp['total'] = 0
                    temp['pct'] = 0
                    # temp['year'] = year
                    # temp['month'] = month
                    # temp['day'] = day
                    temp['hour'] = x
                    temp['period_label'] = f'{x}:00'
                    temp['period'] = temp['period_label']
                    new_summary_over_time.append(temp)
                else:
                    new_summary_over_time.append(curr)
                    idx += 1
    if not new_summary_over_time:
        new_summary_over_time = summary_over_time

    return new_summary_over_time


def get_next_in_date_hierarchy(request, date_hierarchy):
    # 不能调动以下判断顺序，因为要从小到大判断
    if date_hierarchy + '__day' in request.GET:
        return 'hour'
    if date_hierarchy + '__month' in request.GET:
        return 'day'
    if date_hierarchy + '__year' in request.GET:
        return 'month'
    return 'year'


def get_date_hierarchy_year_month_day(request, date_hierarchy):
    year = request.GET.get(date_hierarchy + '__year')
    month = request.GET.get(date_hierarchy + '__month')
    day = request.GET.get(date_hierarchy + '__day')
    return year, month, day


def gen_changelist_title(request, date_hierarchy, model_name):
    year = request.GET.get(date_hierarchy + '__year')
    month = request.GET.get(date_hierarchy + '__month')
    day = request.GET.get(date_hierarchy + '__day')

    title = ''
    if year:
        title += f'{year}年'
    if month:
        title += f'{month}月'
    if day:
        title += f'{day}日'

    if title:
        return f'{title}的{model_name}'
    return f'全部{model_name}'


def get_total_every_period(qs, request, date_hierarchy):
    x_num = 0
    year = None
    month = None
    day = None
    extract_field = date_hierarchy
    next_date_hierarchy = get_next_in_date_hierarchy(request, date_hierarchy)

    # print(date_hierarchy)
    if next_date_hierarchy == 'year':
        # 按年份统计数量
        annotate_options = {'year': ExtractYear(extract_field)}
        values_args = ('year',)
        order_by_args = values_args
    elif next_date_hierarchy == 'month':
        # 按年月统计数量
        annotate_options = {
            'year': ExtractYear(extract_field),
            'month': ExtractMonth(extract_field)
        }
        values_args = ('year', 'month')
        order_by_args = values_args
        x_num = 12
    elif next_date_hierarchy == 'day':
        # 按年月日统计数量
        annotate_options = {
            'year': ExtractYear(extract_field),
            'month': ExtractMonth(extract_field),
            'day': ExtractDay(extract_field),
        }
        values_args = ('year', 'month', 'day')
        order_by_args = values_args

        year = request.GET.get(date_hierarchy + '__year')
        month = request.GET.get(date_hierarchy + '__month')
        x_num = calendar.monthrange(int(year), int(month))[1]

    elif next_date_hierarchy == 'hour':
        # 按年月日时统计数量
        annotate_options = {
            'year': ExtractYear(extract_field),
            'month': ExtractMonth(extract_field),
            'day': ExtractDay(extract_field),
            'hour': ExtractHour(extract_field),
        }
        values_args = ('year', 'month', 'day', 'hour')
        order_by_args = values_args
        x_num = 24
    else:
        # 按年份统计数量
        annotate_options = {}
        values_args = ()
        order_by_args = values_args

    # 统计数量
    total_every_period = qs.annotate(
        **annotate_options
    ).values(*values_args).order_by(*order_by_args).annotate(total=Count('id'))
    return total_every_period, x_num


def gen_summary_over_time(total_every_period, high, low):
    summary_over_time = []
    for x in total_every_period:
        total = x.get('total') or 0
        temp = {
            'total': total,
            'pct': round((total / high) * 100, 2) if high else 0,
        }

        year = x.get('year')
        month = x.get('month')
        day = x.get('day')
        hour = x.get('hour')

        period_label = ''
        if year:
            period_label += f'{year}'
            temp['year'] = year
        if month:
            period_label += f'-{month}'
            temp['month'] = month

        if day:
            period_label += f'-{day}'
            temp['day'] = day
        if hour:
            period_label += f' {hour}:00'
            temp['hour'] = hour

        temp['period_label'] = period_label
        temp['period'] = period_label

        summary_over_time.append(temp)

    return summary_over_time


def get_chart_data(request, qs, date_hierarchy):
    next_date_hierarchy = get_next_in_date_hierarchy(request, date_hierarchy)
    # 统计周期数量
    total_every_period, x_num = get_total_every_period(qs, request, date_hierarchy)

    # 获取最小值和最大值
    total_range = total_every_period.aggregate(low=Min('total'), high=Max('total'))
    # print(total_range)
    high, low = total_range.get('high', 0), total_range.get('low', 0)
    summary_over_time = gen_summary_over_time(total_every_period, high, low)
    # print(summary_over_time)
    year, month, day = get_date_hierarchy_year_month_day(request, date_hierarchy)
    chart_data = fill_empty_date(summary_over_time, x_num, next_date_hierarchy, year, month, day)
    return chart_data


def get_chart_title(request, date_hierarchy):
    next_date_hierarchy = get_next_in_date_hierarchy(request, date_hierarchy)
    date_title_mapping = {
        'year': '按年份统计',
        'month': '按月份统计',
        'day': '按日期统计',
    }
    return date_title_mapping.get(next_date_hierarchy, None)
