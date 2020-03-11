from rest_framework import serializers

from .models import Purchase, Product


class PurchaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Purchase
        fields = [
            'name',
            'purchaser'
        ]


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            'name', 'category', 'in_stock'
        ]
