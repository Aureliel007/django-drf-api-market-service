from rest_framework import serializers

from .models import Product, Category, Order, OrderItem, Contact, Shop, User, ProductParameter



class ShopSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shop
        fields = ('name', )

class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    shop = ShopSerializer(required=False)
    role = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('email', 'username', 'role', 'password', 'shop')

    def validate_role(self, value):
        if value not in [User.ROLE_CHOICES[0][0], User.ROLE_CHOICES[1][0]]:
            raise serializers.ValidationError('Неверное значение роли')
        return value
    
    def create(self, validated_data):
        if validated_data.get('role', 'client') == User.ROLE_CHOICES[1][0]:
            try:
                shop_data = validated_data.pop('shop')
                user = User.objects.create_user(**validated_data)
                Shop.objects.create(user=user, **shop_data)
            except KeyError:
                raise serializers.ValidationError('Введите данные магазина')
        else:
            user = User.objects.create_user(**validated_data)
        return user


class ProductParameterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="parameter.name")
    value = serializers.CharField()

    class Meta:
        model = ProductParameter
        fields = ('name', 'value')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)

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

    def validate_file(self, value):
        if not value.name.endswith('.yml') and not value.name.endswith('.yaml'):
            raise serializers.ValidationError('Неверное расширение файла')
        return value