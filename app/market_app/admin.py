from django.contrib import admin

from .models import User, Product, Order, Contact, Category, Shop

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Contact)
admin.site.register(Category)
admin.site.register(Shop)
