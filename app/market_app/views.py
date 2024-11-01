from rest_framework import generics

from .models import Product, Category, Order, OrderItem, Contact
from .serializers import ProductSerializer


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
