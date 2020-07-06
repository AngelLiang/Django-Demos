from django.db.models import Sum
from slick_reporting.views import SampleReportView
from slick_reporting.fields import BaseReportField

from .models import Order, OrderItem


class OrderItemReportView(SampleReportView):

    # The model where you have the data
    report_model = OrderItem

    # the main date to use if date filter is needed
    date_field = 'order__order_date'
    # date_field support traversing, you can
    # date_field = 'order__date_placed'

    # A foreign key to group calculation on
    group_by = 'product'

    # The columns you want to display , `quantity` and `value` are fields on `MySalesItem` model.
    columns = ['name', BaseReportField.create(Sum, 'quantity'), BaseReportField.create(Sum, 'price')]

    # Another way making use of the built-in Report Fields which is identical to the above
    # columns = ['name', '__total_quantity__',]

    # time_series_pattern = 'monthly'

    # Charts
    charts_settings = [
        {
            'type': 'bar',
            'data_source': '__total_quantity__',
            'title_source': 'name',
        },
    ]
