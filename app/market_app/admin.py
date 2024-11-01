from django.contrib import admin

from .models import User, Product, Order, OrderItem, Contact

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Order)