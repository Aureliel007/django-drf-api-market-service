from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('client', 'Клиент'),
        ('supplier', 'Поставщик'),
    )

    email = models.EmailField(verbose_name='Электронная почта', unique=True)
    username = models.CharField(
        verbose_name='Юзернейм', max_length=80, blank=True, null=True
    )
    role = models.CharField(
        verbose_name='Роль', max_length=10, choices=ROLE_CHOICES
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # @property
    # def is_client(self):
    #     return self.role == 'client'

    # @property
    # def is_supplier(self):
    #     return self.role == 'supplier'

    def __str__(self):
        return f'{self.email} ({self.role})'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Supplier(models.Model):
    user = models.OneToOneField(
        User, verbose_name='Пользователь', on_delete=models.CASCADE
    )
    name = models.CharField(verbose_name='Название', max_length=255)
    is_active_supplier = models.BooleanField(verbose_name='Принимает заказы', default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = "Магазины"

class Category(models.Model):
    name = models.CharField(verbose_name='Название', max_length=255)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(verbose_name='Название', max_length=255)
    description = models.TextField(verbose_name='Описание', blank=True)
    price = models.DecimalField(
        verbose_name='Цена', max_digits=10, decimal_places=2
    )
    category = models.ForeignKey(
        Category, verbose_name='Категория', on_delete=models.CASCADE
    )
    supplier = models.ForeignKey(
        Supplier, verbose_name='Поставщик', on_delete=models.CASCADE
    )
    available_stock = models.PositiveIntegerField(verbose_name='Доступное количество')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = "Товары"

class Parameter(models.Model):
    name = models.CharField(verbose_name='Название параметра', max_length=255, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Параметр продукта'
        verbose_name_plural = 'Параметры продуктов'

class ProductParameter(models.Model):
    product = models.ForeignKey(
        Product, verbose_name='Товар', on_delete=models.CASCADE
    )
    parameter = models.ForeignKey(
        Parameter, verbose_name='Параметр', on_delete=models.CASCADE
    )
    value = models.CharField(verbose_name='Значение', max_length=255)

    def __str__(self):
        return f'{self.product}: {self.parameter.name} - {self.value}'
    
    class Meta:
        verbose_name = 'Параметр продукта'
        verbose_name_plural = 'Параметры продуктов'

class Order(models.Model):
    STATUS_CHOICES = (
        ('new', 'Создан'),
        ('in_progress', 'Собирается'),
        ('shipping', 'Передан в доставку'),
        ('completed', 'Завершен'),
        ('canceled', 'Отменен'),
    )
    user = models.ForeignKey(
        User, verbose_name='Пользователь', on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    status = models.CharField(
        verbose_name='Статус', max_length=20, choices=STATUS_CHOICES, default='new'
    )
    total_price = models.DecimalField(
        verbose_name='Общая цена', max_digits=10, decimal_places=2
    )

    def __str__(self):
        return f'Заказ №{self.id} от {self.created_at.strftime("%d.%m.%Y %H:%M")} - {self.status}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, verbose_name='Заказ', on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, verbose_name='Товар', on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(verbose_name='Количество')

class Contact(models.Model):
    user = models.ForeignKey(
        User, verbose_name='Пользователь', on_delete=models.CASCADE
    )
    city = models.CharField(verbose_name='Город', max_length=100)
    street = models.CharField(verbose_name='Улица', max_length=100)
    house = models.CharField(verbose_name='Дом', max_length=10)
    building = models.CharField(verbose_name='Строение', max_length=10, blank=True)
    flat = models.IntegerField(verbose_name='Квартира', blank=True)
    phone = models.CharField(verbose_name='Телефон', max_length=20)

    def __str__(self):
        return f'{self.city}, улица {self.street}, дом {self.house} {self.building}, кв. {self.flat}'