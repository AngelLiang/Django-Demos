
from rest_framework import viewsets
from tyadmin_api.custom import XadminViewSet
from django.contrib.auth.models import Permission, Group, User
from django.contrib.contenttypes.models import ContentType
from order.models import Customer, Product, Order, OrderItem

from tyadmin_api.auto_serializers import PermissionListSerializer, GroupListSerializer, UserListSerializer, ContentTypeListSerializer, CustomerListSerializer, ProductListSerializer, OrderListSerializer, OrderItemListSerializer
from tyadmin_api.auto_serializers import PermissionCreateUpdateSerializer, GroupCreateUpdateSerializer, UserCreateUpdateSerializer, ContentTypeCreateUpdateSerializer, CustomerCreateUpdateSerializer, ProductCreateUpdateSerializer, OrderCreateUpdateSerializer, OrderItemCreateUpdateSerializer
from tyadmin_api.auto_filters import PermissionFilter, GroupFilter, UserFilter, ContentTypeFilter, CustomerFilter, ProductFilter, OrderFilter, OrderItemFilter
    
    
class PermissionViewSet(XadminViewSet):
        serializer_class = PermissionListSerializer
        queryset = Permission.objects.all().order_by('-pk')
        filter_class = PermissionFilter
        search_fields = ["name","codename"]

        def get_serializer_class(self):
            if self.action == "list":
                return PermissionListSerializer
            else:
                return PermissionCreateUpdateSerializer

    
class GroupViewSet(XadminViewSet):
        serializer_class = GroupListSerializer
        queryset = Group.objects.all().order_by('-pk')
        filter_class = GroupFilter
        search_fields = ["name"]

        def get_serializer_class(self):
            if self.action == "list":
                return GroupListSerializer
            else:
                return GroupCreateUpdateSerializer

    
class UserViewSet(XadminViewSet):
        serializer_class = UserListSerializer
        queryset = User.objects.all().order_by('-pk')
        filter_class = UserFilter
        search_fields = ["password","username","first_name","last_name","email"]

        def get_serializer_class(self):
            if self.action == "list":
                return UserListSerializer
            else:
                return UserCreateUpdateSerializer

    
class ContentTypeViewSet(XadminViewSet):
        serializer_class = ContentTypeListSerializer
        queryset = ContentType.objects.all().order_by('-pk')
        filter_class = ContentTypeFilter
        search_fields = ["app_label","model"]

        def get_serializer_class(self):
            if self.action == "list":
                return ContentTypeListSerializer
            else:
                return ContentTypeCreateUpdateSerializer

    
class CustomerViewSet(XadminViewSet):
        serializer_class = CustomerListSerializer
        queryset = Customer.objects.all().order_by('-pk')
        filter_class = CustomerFilter
        search_fields = ["name","phone"]

        def get_serializer_class(self):
            if self.action == "list":
                return CustomerListSerializer
            else:
                return CustomerCreateUpdateSerializer

    
class ProductViewSet(XadminViewSet):
        serializer_class = ProductListSerializer
        queryset = Product.objects.all().order_by('-pk')
        filter_class = ProductFilter
        search_fields = ["name"]

        def get_serializer_class(self):
            if self.action == "list":
                return ProductListSerializer
            else:
                return ProductCreateUpdateSerializer

    
class OrderViewSet(XadminViewSet):
        serializer_class = OrderListSerializer
        queryset = Order.objects.all().order_by('-pk')
        filter_class = OrderFilter
        search_fields = ["title"]

        def get_serializer_class(self):
            if self.action == "list":
                return OrderListSerializer
            else:
                return OrderCreateUpdateSerializer

    
class OrderItemViewSet(XadminViewSet):
        serializer_class = OrderItemListSerializer
        queryset = OrderItem.objects.all().order_by('-pk')
        filter_class = OrderItemFilter
        search_fields = []

        def get_serializer_class(self):
            if self.action == "list":
                return OrderItemListSerializer
            else:
                return OrderItemCreateUpdateSerializer
