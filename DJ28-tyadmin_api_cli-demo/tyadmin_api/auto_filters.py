from django_filters import rest_framework as filters
from tyadmin_api.custom import DateFromToRangeFilter
from django.contrib.auth.models import Permission, Group, User
from django.contrib.contenttypes.models import ContentType
from order.models import Customer, Product, Order, OrderItem


class PermissionFilter(filters.FilterSet):
    content_type_text = filters.CharFilter(field_name="content_type")

    class Meta:
        model = Permission
        exclude = []


class GroupFilter(filters.FilterSet):

    class Meta:
        model = Group
        exclude = []


class UserFilter(filters.FilterSet):
    last_login = DateFromToRangeFilter(field_name="last_login")
    date_joined = DateFromToRangeFilter(field_name="date_joined")

    class Meta:
        model = User
        exclude = []


class ContentTypeFilter(filters.FilterSet):

    class Meta:
        model = ContentType
        exclude = []


class CustomerFilter(filters.FilterSet):

    class Meta:
        model = Customer
        exclude = []


class ProductFilter(filters.FilterSet):

    class Meta:
        model = Product
        exclude = []


class OrderFilter(filters.FilterSet):
    customer_text = filters.CharFilter(field_name="customer")

    class Meta:
        model = Order
        exclude = []


class OrderItemFilter(filters.FilterSet):
    order_text = filters.CharFilter(field_name="order")
    product_text = filters.CharFilter(field_name="product")

    class Meta:
        model = OrderItem
        exclude = []