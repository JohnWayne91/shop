from decimal import Decimal
from unittest import mock

from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model

from .models import Category, Product, Customer, Cart, CartProduct, Order
from .utils import recalculate_cart
from .views import AddToCartView, BaseView

User = get_user_model()


class ShopTestCases(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username='testuser', password='password')
        self.category = Category.objects.create(name='Notebooks')
        image ="ASUS-ROG-Strix-SCAR-15-G532LWS-2.jpg"
        self.notebook = Product.objects.create(
            category=self.category,
            title='Test notebook',
            slug='test-slug',
            image=image,
            price=Decimal('50000.00'),
            specifications={
                "diagonal": "17.3",
                "color": "black",
                "RAM": "8",
                "Video": "GeForce 1660"
            }
        )
        self.customer = Customer.objects.create(user=self.user, phone='111111111222', address='Address')
        self.cart = Cart.objects.create(owner=self.customer)
        self.cart_product = CartProduct.objects.create(
            user=self.customer,
            cart=self.cart,
            product=self.notebook
        )

    def test_add_to_cart(self):
        self.cart.products.add(self.cart_product)
        recalculate_cart(self.cart)
        self.assertIn(self.cart_product, self.cart.products.all())
        self.assertEqual(self.cart.products.count(), 1)
        self.assertEqual(self.cart.total_price, Decimal('50000.00'))

    def test_change_cart_product_amount(self):
        self.cart.products.add(self.cart_product)
        recalculate_cart(self.cart)
        self.cart_product.amount = 4
        self.cart_product.save()
        recalculate_cart(self.cart)
        self.assertEqual(self.cart.total_price, Decimal('200000.00'))
        self.assertEqual(self.cart.products.count(), 1)

    def test_delete_product_from_cart(self):
        self.cart.products.add(self.cart_product)
        recalculate_cart(self.cart)
        self.cart.products.remove(self.cart_product)
        recalculate_cart(self.cart)
        self.assertEqual(self.cart.total_price, Decimal('0.00'))
        self.assertEqual(self.cart.products.count(), 0)

    def test_response_from_add_to_cart_view(self):
        factory = RequestFactory()
        request = factory.get('')
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        request.user = self.user
        response = AddToCartView.as_view()(request, slug='test-slug')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/cart/')

    def test_mock_homepage(self):
        mock_data = mock.Mock(status_code=444)
        with mock.patch('mainapp.views.BaseView.get', return_value=mock_data) as mock_data_:
            factory = RequestFactory()
            request = factory.get('')
            request.user = self.user
            response = BaseView.as_view()(request)
            self.assertEqual(response.status_code, 444)






