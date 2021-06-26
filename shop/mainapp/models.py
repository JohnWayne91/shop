import sys
from io import BytesIO
from PIL import Image

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse
from django.utils import timezone

from .utils import resize_image


User = get_user_model()


def get_models_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]


class LatestProductsManager:

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):  # represent several product models in one
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(
                        products, key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to), reverse=True
                    )
        return products


class LatestProducts:
    objects = LatestProductsManager()


class CategoryManager(models.Manager):
    CATEGORY_NAME_COUNT_NAME = {
        'Notebooks': 'notebook__count',
        'Smartphones': 'smartphone__count'
    }

    def get_queryset(self):
        return super().get_queryset()

    def get_categories_for_left_sidebar(self):
        models = get_models_for_count('smartphone', 'notebook')
        qs = list(self.get_queryset().annotate(*models))
        data = [
            dict(name=c.name, url=c.get_absolute_url(), count=getattr(c, self.CATEGORY_NAME_COUNT_NAME[c.name]))
            for c in qs
        ]
        return data


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Category name')
    slug = models.SlugField(unique=True)
    objects = CategoryManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):
    MIN_RESOLUTION = (400, 400)
    MAX_RESOLUTION = (1000, 1000)
    MAX_IMAGE_SIZE = 3145728

    class Meta:
        abstract = True

    category = models.ForeignKey(Category, verbose_name='category', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Product name')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='image', null=True)
    description = models.TextField(verbose_name='description', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='price')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        ct_model = self.__class__._meta.model_name
        return reverse('product_detail', kwargs={'ct_model': ct_model, 'slug': self.slug})

    def get_model_name(self):
        return self.__class__.__name__.lower()

    def save(self, *args, **kwargs):
        resize_image(self, *args, **kwargs)
        super().save(*args, **kwargs)


class CartProduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name='Customer', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart1', verbose_name='cart product', on_delete=models.CASCADE,
                             related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    amount = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Total_price')

    def __str__(self):
        return f'Product: {self.content_object.title} (for the cart)'

    def save(self, *args, **kwargs):
        self.total_price = self.amount * self.content_object.price
        super().save(*args, **kwargs)


class Cart1(models.Model):
    owner = models.ForeignKey('Customer', null=True, verbose_name='owner of the cart', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    products_amount = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Total_price')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    # def save(self, *args, **kwargs):
    #     try:
    #         cart_data = self.products.aggregate(models.Sum('total_price'), models.Count('id'))
    #         if cart_data.get('total_price__sum'):
    #             self.total_price = cart_data['total_price__sum']
    #         else:
    #             self.total_price = 0
    #         self.products_amount = cart_data['id__count']
    #     except:
    #         pass
    #     super().save(*args, **kwargs)


class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name='Customer', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Phone number', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Address', null=True, blank=True)
    orders = models.ManyToManyField('Order', blank=True, related_name='related_customer', verbose_name="Customer's orders")

    def __str__(self):
        return f'Customer: {self.user.first_name} {self.user.last_name}'


class Notebook(Product):
    diagonal = models.CharField(max_length=255, verbose_name='Screen diagonal')
    display_type = models.CharField(max_length=255, verbose_name='display matrix type')
    processor_freq = models.CharField(max_length=255, verbose_name='Processor frequency')
    ram = models.CharField(max_length=255, verbose_name='RAM')
    video = models.CharField(max_length=255, verbose_name='Video card')
    time_without_charge = models.CharField(max_length=255, verbose_name='Time-running without charging')

    def __str__(self):
        return f'{self.category.name} : {self.title}'


class Smartphone(Product):
    diagonal = models.CharField(max_length=255, verbose_name='Screen diagonal')
    display_type = models.CharField(max_length=255, verbose_name='display matrix type')
    resolution = models.CharField(max_length=255, verbose_name='Resolution')
    battery_volume = models.CharField(max_length=255, verbose_name='Battery volume')
    ram = models.CharField(max_length=255, verbose_name='RAM')
    sd = models.BooleanField(default=True, verbose_name='Sd slot')
    sd_memory_max = models.CharField(max_length=255, null=True, blank=True, verbose_name='Maximum memory capacity')
    main_cam_mp = models.CharField(max_length=255, verbose_name='Main camera')
    front_cam_mp = models.CharField(max_length=255, verbose_name='Front camera')

    def __str__(self):
        return f'{self.category.name} : {self.title}'


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
    cart = models.ForeignKey(Cart1, verbose_name='Cart', on_delete=models.CASCADE, null=True, blank=True)
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


