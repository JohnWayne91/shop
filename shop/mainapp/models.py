from django.db import models
from django.db.models import JSONField
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from .utils import resize_image


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Category name')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):
    MIN_RESOLUTION = (400, 400)
    MAX_RESOLUTION = (1000, 1000)
    MAX_IMAGE_SIZE = 3145728

    category = models.ForeignKey(Category, verbose_name='category', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Product name')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='image', null=True)
    description = models.TextField(verbose_name='description', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='price')
    specifications = JSONField(verbose_name='Specifications', null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def get_model_name(self):
        return self.__class__.__name__.lower()

    def save(self, *args, **kwargs):
        resize_image(self, *args, **kwargs)
        super().save(*args, **kwargs)


class CartProduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name='Customer', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Product in the cart', on_delete=models.CASCADE,
                             related_name='related_products')
    product = models.ForeignKey(Product, verbose_name='Product', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Total_price')

    def __str__(self):
        return f'{self.product.title} x {self.amount}'

    def save(self, *args, **kwargs):
        self.total_price = self.amount * self.product.price
        super().save(*args, **kwargs)


class Cart(models.Model):
    owner = models.ForeignKey('Customer', null=True, verbose_name='owner of the cart', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    products_amount = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Total_price')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name='Customer', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Phone number', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Address', null=True, blank=True)
    orders = models.ManyToManyField('Order', blank=True, related_name='related_customer', verbose_name="Customer's orders")

    def __str__(self):
        return f'Customer: {self.user.first_name} {self.user.last_name}'


class Order(models.Model):

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'
    STATUS_PAYED = 'payed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_PAYED, 'Order has been payed'),
        (STATUS_NEW, 'New order'),
        (STATUS_IN_PROGRESS, 'Order in progress'),
        (STATUS_READY, 'Order is ready'),
        (STATUS_COMPLETED, 'Order is completed')
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Pickup'),
        (BUYING_TYPE_DELIVERY, 'Delivery')
    )

    customer = models.ForeignKey(
        Customer, verbose_name='Customer', related_name='related_orders', on_delete=models.CASCADE
    )
    first_name = models.CharField(max_length=255, verbose_name='First name')
    last_name = models.CharField(max_length=255, verbose_name='Last name')
    phone = models.CharField(max_length=20, verbose_name='Phone number')
    cart = models.ForeignKey(Cart, verbose_name='Cart', on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=500, verbose_name='Address', null=True, blank=True)
    status = models.CharField(max_length=100, verbose_name='Order status', choices=STATUS_CHOICES, default=STATUS_NEW)
    buying_type = models.CharField(
        max_length=100, verbose_name='Order type', choices=BUYING_TYPE_CHOICES, default=BUYING_TYPE_SELF
    )
    comment = models.TextField(verbose_name='Comment to order', null=True, blank=True)
    order_creation_date = models.DateTimeField(auto_now=True, verbose_name='Order creation date')
    order_completion_date = models.DateField(verbose_name='Order_completion_date', default=timezone.now)

    def __str__(self):
        return str(self.id)


