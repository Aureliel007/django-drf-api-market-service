from django_filters import rest_framework as filters

from .models import Product


class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    category = filters.CharFilter(field_name='category__name', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['name', 'min_price', 'max_price', 'category']