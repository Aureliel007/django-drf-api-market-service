from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from django.urls import reverse
from model_bakery import baker

from market_app.models import User, Product, Order, OrderItem, Contact


class UserTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "securepassword",
            "role": "client"
        }
        response = self.client.post("/api/v1/register/", data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_user_login(self):
        user = baker.make(User, username="testuser", is_active=True)
        user.set_password("securepassword")
        user.save()
        data = {"username": user.username, "password": "securepassword"}
        response = self.client.post("/api/v1/login/", data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.data)


class ProductTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = baker.make(User, role="client", is_active=True)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

    def test_add_to_cart(self):
        product = baker.make(Product, quantity=10)
        data = {"quantity": 2}
        response = self.client.post(f"/api/v1/products/{product.id}/add_to_cart/", data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Order.objects.filter(user=self.user, status="basket").exists())
        self.assertTrue(OrderItem.objects.filter(order__user=self.user, product=product).exists())

    def test_remove_from_cart(self):
        product = baker.make(Product, quantity=10)
        cart = baker.make(Order, user=self.user, status="basket")
        baker.make(OrderItem, order=cart, product=product, quantity=5)

        response = self.client.post(f"/api/v1/products/{product.id}/remove_from_cart/")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(OrderItem.objects.filter(order=cart, product=product).exists())


class OrderTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = baker.make(User, role="client", is_active=True)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

    def test_show_cart(self):
        cart = baker.make(Order, user=self.user, status="basket")
        baker.make(OrderItem, order=cart, _quantity=3)

        response = self.client.get("/api/v1/orders/show_cart/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("order_items", response.data)

    def test_confirm_order(self):
        contact = baker.make(Contact, user=self.user)
        product = baker.make(Product, quantity=10)
        cart = baker.make(Order, user=self.user, status="basket")
        baker.make(OrderItem, order=cart, product=product, quantity=5)

        data = {"address_id": contact.id}
        response = self.client.post("/api/v1/orders/confirm_order/", data)
        self.assertEqual(response.status_code, 200)
        cart.refresh_from_db()
        product.refresh_from_db()
        self.assertEqual(cart.status, "confirmed")
        self.assertEqual(product.quantity, 5)
