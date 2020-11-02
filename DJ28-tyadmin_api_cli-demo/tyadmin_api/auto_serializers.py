from rest_framework import serializers
from django.contrib.auth.models import Permission, Group, User
from django.contrib.contenttypes.models import ContentType
from order.models import Customer, Product, Order, OrderItem


class ContentTypeListSerializer(serializers.ModelSerializer):
    

    key = serializers.CharField(source="pk")
    ty_options_display_txt = serializers.SerializerMethodField()

    class Meta:
        model = ContentType
        fields = "__all__"

    @staticmethod
    def get_ty_options_display_txt(obj):
        return str(obj)


class ContentTypeCreateUpdateSerializer(serializers.ModelSerializer):
    
    ty_options_display_txt = serializers.SerializerMethodField()
    class Meta:
        model = ContentType
        fields = "__all__"
    @staticmethod
    def get_ty_options_display_txt(obj):
        return str(obj)


class CustomerListSerializer(serializers.ModelSerializer):
    

    key = serializers.CharField(source="pk")
    ty_options_display_txt = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = "__all__"

    @staticmethod
    def get_ty_options_display_txt(obj):
        return str(obj)


class CustomerCreateUpdateSerializer(serializers.ModelSerializer):
    
    ty_options_display_txt = serializers.SerializerMethodField()
    class Meta:
        model = Customer
        fields = "__all__"
    @staticmethod
    def get_ty_options_display_txt(obj):
        return str(obj)


class ProductListSerializer(serializers.ModelSerializer):
    

    key = serializers.CharField(source="pk")
    ty_options_display_txt = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"

    @staticmethod
    def get_ty_options_display_txt(obj):
        return str(obj)


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    
    ty_options_display_txt = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = "__all__"
    @staticmethod
    def get_ty_options_display_txt(obj):
        return str(obj)


class PermissionListSerializer(serializers.ModelSerializer):
    
    content_type = ContentTypeCreateUpdateSerializer()

    key = serializers.CharField(source="pk")
    ty_options_display_txt = serializers.SerializerMethodField()

    class Meta:
        model = Permission
        fields = "__all__"

    @staticmethod
    def get_ty_options_display_txt(obj):
        return str(obj)


class PermissionCreateUpdateSerializer(serializers.ModelSerializer):
    
    ty_options_display_txt = serializers.SerializerMethodField()
    class Meta:
        model = Permission
        fields = "__all__"
    @staticmethod
    def get_ty_options_display_txt(obj):
        return str(obj)


class GroupListSerializer(serializers.ModelSerializer):
    
    permissions = PermissionCreateUpdateSerializer(many=True)

    key = serializers.CharField(source="pk")
    ty_options_display_txt = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = "__all__"

    @staticmethod
    def get_ty_options_display_txt(obj):
        return str(obj)


class GroupCreateUpdateSerializer(serializers.ModelSerializer):
    
    ty_options_display_txt = serializers.SerializerMethodField()
    class Meta:
        model = Group
        fields = "__all__"
    @staticmethod
    def get_ty_options_display_txt(obj):
        return str(obj)


class UserListSerializer(serializers.ModelSerializer):
    
    groups = GroupCreateUpdateSerializer(many=True)
    user_permissions = PermissionCreateUpdateSerializer(many=True)

    key = serializers.CharField(source="pk")
    ty_options_display_txt = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = "__all__"

    @staticmethod
    def get_ty_options_display_txt(obj):
        return str(obj)


class UserCreateUpdateSerializer(serializers.ModelSerializer):
    
    ty_options_display_txt = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = "__all__"
    @staticmethod
    def get_ty_options_display_txt(obj):
        return str(obj)


class OrderListSerializer(serializers.ModelSerializer):
    
    customer = CustomerCreateUpdateSerializer()

    key = serializers.CharField(source="pk")
    ty_options_display_txt = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"

    @staticmethod
    def get_ty_options_display_txt(obj):
        return str(obj)


class OrderCreateUpdateSerializer(serializers.ModelSerializer):
    
    ty_options_display_txt = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = "__all__"
    @staticmethod
    def get_ty_options_display_txt(obj):
        return str(obj)


class OrderItemListSerializer(serializers.ModelSerializer):
    
    order = OrderCreateUpdateSerializer()
    product = ProductCreateUpdateSerializer()

    key = serializers.CharField(source="pk")
    ty_options_display_txt = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = "__all__"

    @staticmethod
    def get_ty_options_display_txt(obj):
        return str(obj)


class OrderItemCreateUpdateSerializer(serializers.ModelSerializer):
    
    ty_options_display_txt = serializers.SerializerMethodField()
    class Meta:
        model = OrderItem
        fields = "__all__"
    @staticmethod
    def get_ty_options_display_txt(obj):
        return str(obj)
