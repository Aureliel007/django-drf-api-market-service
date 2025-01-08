from django.contrib import admin

from .models import User, Product, Order, Contact, Category, Shop


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'name', 'model', 'category', 'shop', 'price', 'price_rrc', 'quantity')
    list_display_links = ('id', 'external_id', 'name')
    list_per_page = 20
    search_fields = ('name', 'model', 'category__name', 'shop__name')
    list_filter = ('category__name', 'shop__name')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'role')
    list_display_links = ('id', 'username', 'email')
    list_per_page = 20

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('info', 'user', 'created_at', 'status')
    list_display_links = ('info', )
    list_per_page = 20

    def info(self, order: Order):
        return order

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'user__id', 'user__email')
    list_display_links = ('id', 'user__id', 'user__email')
    list_per_page = 20

    def address(self, contact: Contact):
        return contact

admin.site.register(Category)
admin.site.register(Shop)
