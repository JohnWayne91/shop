from decimal import Decimal
from PIL import Image

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Category, Notebook, Customer, Cart1, CartProduct
from .utils import recalculate_cart

User = get_user_model()


class ShopTestCases(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username='testuser', password='password')
        self.category = Category.objects.create(name='Notebooks')
        image ="notebook3_s7C8Rqa.jpg"
        self.notebook = Notebook.objects.create(
            category=self.category,
            title='Test notebook',
            slug='test-slug',
            image=image,
            price=Decimal('50000.00'),
            diagonal='17.3',
            display_type='IPS',
            processor_freq='3.4 Ghz',
            ram='8 Gb',
            video='GeForce GTX 1060 3Gb',
            time_without_charge='4h'
        )
        self.customer = Customer.objects.create(user=self.user, phone='111111111222', address='Address')
        self.cart = Cart1.objects.create(owner=self.customer)
        self.cart_product = CartProduct.objects.create(
            user=self.customer,
            cart=self.cart,
            content_object=self.notebook
        )

    def test_add_to_cart(self):
        self.cart.products.add(self.cart_product)
        recalculate_cart(self.cart)
        self.assertIn(self.cart_product, self.cart.products.all())
        self.assertEqual(self.cart.products.count(), 1)
        self.assertEqual(self.cart.total_price, Decimal('50000.00'))





