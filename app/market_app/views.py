import yaml
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated 
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import MethodNotAllowed
from django_filters.rest_framework import DjangoFilterBackend

from market_api_service.settings import EMAIL_HOST_USER
from .permissions import IsShopOwner, IsOwner, IsOwnerOrAdminOrReadOnly
from .models import (Product, Order, OrderItem, Contact, User)
from .serializers import (
    CreateUserSerializer, PriceListUploadSerializer, ProductSerializer,
    ContactSerializer, OrderSerializer
)
from .tasks import update_products_from_data, send_email
from .filters import ProductFilter


class CreateUser(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_email.delay(
                subject='Добро пожаловать в Наш Магазин',
                user_email=user.email,
                message=f'Добро пожаловать в Наш Магазин, {user.username}!'
            )
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
    return Response(
        {'error': 'Некорректный логин или пароль'},
        status=status.HTTP_401_UNAUTHORIZED
    )


class ProductList(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    # запрещаю метод POST, потому что загрузка товаров осуществляется через прайс-лист
    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed('POST')

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_to_cart(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        quantity = int(request.data.get('quantity', 1))
        if quantity > product.quantity:
            return Response(
                {'message': f'Недостаточно товара на складе, в наличии {product.quantity}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        cart, created = Order.objects.get_or_create(user=request.user, status='basket')
        if created:
            cart.save()
        OrderItem.objects.update_or_create(order=cart, product=product, defaults={'quantity': quantity})
        return Response(
            {'message': 'Товар добавлен в корзину'},
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def remove_from_cart(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        try: 
            cart = Order.objects.get(user=request.user, status='basket')
        except Order.DoesNotExist:
            return Response(
                {'message': 'Корзина не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            item = OrderItem.objects.get(order=cart, product=product)
        except OrderItem.DoesNotExist:
            return Response(
                {'message': 'Товар не найден в корзине'},
                status=status.HTTP_404_NOT_FOUND
            )
        item.delete()
        return Response(
            {'message': 'Товар удален из корзины'},
            status=status.HTTP_200_OK
        )

class OrderViewSet(ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).exclude(status='basket')
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def show_cart(self, request):
        try:
            cart = Order.objects.get(user=request.user, status='basket')
        except Order.DoesNotExist:
            return Response(
                {'message': 'Корзина пуста'},
                status=status.HTTP_200_OK
            )
        serializer = self.get_serializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def confirm_order(self, request):
        address = request.data.get('address_id', None)
        if not address:
            return Response(
                {'message': 'Укажите адрес доставки'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            contact = Contact.objects.get(id=address)
        except Contact.DoesNotExist:
            return Response(
                {'message': 'Адрес не найден'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            cart = Order.objects.get(user=request.user, status='basket')
        except Order.DoesNotExist:
            return Response(
                {'message': 'Корзина пуста'},
                status=status.HTTP_400_BAD_REQUEST
            )
        products = Product.objects.filter(orderitem__order=cart)

        for product in products:
            order_quantity = product.orderitem_set.get(order=cart).quantity
            fact_quantity = product.quantity
            if order_quantity > fact_quantity:
                return Response(
                    {'message': f'Недостаточно товара на складе, в наличии {fact_quantity}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            product.quantity -= order_quantity
            product.save()

        cart.status = 'confirmed'
        cart.save()
        send_email.delay(
            subject='Подтверждение заказа',
            message=f'Ваш заказ №{cart.id} был успешно подтвержден и находится в обработке.\n',
            user_email=request.user.email
        )
        return Response(
            {'message': 'Заказ успешно оформлен'},
            status=status.HTTP_200_OK
        )

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

            update_products_from_data.delay(data, shop_id)
            return Response({"status": "Импорт завершен"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ContactList(ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

