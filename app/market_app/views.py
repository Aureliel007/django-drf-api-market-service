from django.shortcuts import get_object_or_404
import yaml
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token

from .permissions import IsShopOwner
from .models import (
    Parameter, Product, Category, ShopCategory, Order, OrderItem, Contact, 
    ProductParameter, Shop, User
)
from .serializers import CreateUserSerializer, PriceListUploadSerializer, ProductSerializer
from .product_utils import update_products_from_data


class CreateUser(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def user_login(request):
    data = request.data
    username = data.get('username')
    password = data.get('password')
    user = User.objects.filter(username=username).first()
    if user is not None and user.check_password(password):
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    return Response({'error': 'Некорректный логин или пароль'}, status=status.HTTP_401_UNAUTHORIZED)


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_to_cart(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        cart = Order.objects.get_or_create(user=request.user, status='basket')[0]
        OrderItem.objects.get_or_create(order=cart, product=product, quantity=1)
        return Response({'message': 'Товар добавлен в корзину'}, status=status.HTTP_201_CREATED)

class PriceListUploadView(APIView):
    permission_classes = [IsAuthenticated, IsShopOwner]
    def post(self, request, *args, **kwargs):
        serializer = PriceListUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            shop = request.user.shop
            shop_id = shop.id

            # Обработка и обновление продуктов из YML
            file_data = file.read().decode("utf-8")
            data = yaml.safe_load(file_data)

            update_products_from_data(data, shop_id)
            return Response({"status": "Импорт завершен"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

