import yaml
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import (
    Parameter, Product, Category, ShopCategory, Order, OrderItem, Contact, ProductParameter, Shop
)
from .serializers import PriceListUploadSerializer, ProductSerializer
from .product_utils import update_products_from_data


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class PriceListUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PriceListUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            shop_id = serializer.validated_data['shop_id']

            # Обработка и обновление продуктов из YML
            file_data = file.read().decode("utf-8")
            data = yaml.safe_load(file_data)

            update_products_from_data(data, shop_id)
            return Response({"status": "Импорт завершен"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

