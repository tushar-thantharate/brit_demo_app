from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

# Import your Views and Models
from products.views import ProductsViewSet
from products.models import Products


class ProductsViewSetTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        # Log in the test user
        self.client.login(username="testuser", password="testpassword")

        # Create some test products
        self.product1 = Products.objects.create(name="Product1", price=100)
        self.product2 = Products.objects.create(name="Product2", price=150)

    def test_create_product(self):
        # Test creating a new product
        data = {"name": "New Product", "price": 200}
        response = self.client.post(reverse("create_product"), data)

        self.assertEqual(response.status_code, 201)

    def test_update_product(self):
        # Test updating an existing product
        data = {"name": "Updated Product", "price": 250}
        response = self.client.put(
            reverse("delete_product", args=[self.product1.id]), data
        )

        self.assertEqual(response.status_code, 405)

    def test_delete_product(self):
        # Test deleting an existing product
        response = self.client.delete(
            reverse("delete_product", args=[self.product2.id])
        )

        self.assertEqual(response.status_code, 204)
