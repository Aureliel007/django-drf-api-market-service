from rest_framework import serializers

from .models import Product, Category, Order, OrderItem, Contact, Shop, Parameter, ProductParameter


class ParameterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Parameter
        fields = ('name',)

class ProductParameterSerializer(serializers.ModelSerializer):
    parameter = ParameterSerializer()

    class Meta:
        model = ProductParameter
        fields = ('parameter', 'value')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('id', 'name')

class ProductSerializer(serializers.ModelSerializer):
    parameters = ProductParameterSerializer(many=True)
    category = CategorySerializer()
    shop = ShopSerializer()

    class Meta:
        model = Product
        fields = (
            'id',
            'external_id',
            'name',
            'model',
            'category',
            'shop',
            'price',
            'price_rrc',
            'quantity',
            'parameters'
        )







class PriceListUploadSerializer(serializers.Serializer):

    file = serializers.FileField()
    shop_id = serializers.IntegerField()

    def validate_file(self, value):
        if not value.name.endswith('.yml') and not value.name.endswith('.yaml'):
            raise serializers.ValidationError('Неверное расширение файла')
        return value