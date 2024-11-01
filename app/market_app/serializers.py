from rest_framework import serializers

from .models import Product, Category, Order, OrderItem, Contact


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'description',
            'price',
            'category',
            'supplier',
            'available_stock',
        )