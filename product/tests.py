from django.test import TestCase
from .models import Product
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.urls import reverse


class ProductModelTest(TestCase):

    def test_product_creation(self):
        product = Product.objects.create(
            name = "Laptop",
            price = Decimal('999.99'),
            stock = 10,
            discount = Decimal('50.00')
        )
        self.assertEqual(product.name, "Laptop")
        self.assertEqual(product.price, Decimal('999.99'))
        self.assertEqual(product.stock, 10)
        self.assertEqual(product.is_active, True)
        self.assertEqual(product.discount, Decimal('50.00'))

    def test_name_min_length(self):
        product = Product(
            name = "La",
            price = Decimal('999.99'),
            stock = 10,
            discount = Decimal('50.00')
        )
    
        with self.assertRaises(ValidationError):
            product.full_clean()


    def test_discount_not_exceed_price(slef):
        product = Product(
            name = "Laptop",
            price = Decimal('400.99'),
            stock = 10,
            discount = Decimal('500.00')
        )
        with slef.assertRaises(ValidationError):
            product.full_clean()

    def test_stock_zero_deactivates(self):
        product = Product(
            name = "Laptop",
            price = Decimal('999.99'),
            stock = 0,
            discount = Decimal('50.00')
        )
        product.full_clean()
        product.save()
        self.assertFalse(product.is_active)


    def test_final_price_cal(self):
        product = Product(
            name = "Laptop",
            price = Decimal('500.00'),
            stock = 10,
            discount = Decimal('50.00')
        )
        self.assertEqual(product.final_price(), 450.00)

class ProductViewTest(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name = "Phone",
            price = Decimal('500.00'),
            stock = 10,
            discount = Decimal('50.00')
        )

    def test_product_list_view(self):
        response = self.client.get(reverse("product_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Phone")

    def test_product_details_view(self):
        response = self.client.get(reverse("product_detail", args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Phone")
        
    def test_product_create_view(self):
        response = self.client.post(reverse("product_create"),{
            "name":"Tablet", "price":"300.00", "stock":"5", "discount": "50.00"
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Product.objects.count(), 2)

    def test_product_update_view(self):
        response = self.client.post(reverse("product_update", args=[self.product.id]),{
            "name":"Update Tablet", "price":"300.00", "stock":"5", "discount": "50.00"
        })
        self.assertEqual(response.status_code, 302)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Update Tablet")

    def test_delete_product_view(self):
        response = self.client.post(reverse("product_delete", args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Product.objects.count(), 0)