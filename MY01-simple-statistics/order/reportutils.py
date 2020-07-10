

def fill_empty_date(summary_over_time, x_num, date_hierarchy, year, month, day):
    idx = 0
    new_summary_over_time = []
    if len(summary_over_time) != x_num:
        if date_hierarchy == 'month':
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
        elif date_hierarchy == 'day':
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
        elif date_hierarchy == 'hour':
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
