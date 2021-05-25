import sys
from io import BytesIO

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from PIL import Image


User = get_user_model()


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


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Category name')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    MIN_RESOLUTION = (400, 400)
    MAX_RESOLUTION = (1000, 1000)
    MAX_IMAGE_SIZE = 3145728

    class Meta:
        abstract = True

    category = models.ForeignKey(Category, verbose_name='category', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Product name')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='image')
    description = models.TextField(verbose_name='description', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='price')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        image = self.image
        img = Image.open(image)
        min_height, min_width = self.MIN_RESOLUTION
        max_height, max_width = self.MAX_RESOLUTION
        if image.size > self.MAX_IMAGE_SIZE:
            raise ValidationError('The size of the uploaded image is more than 3 MB')
        if img.height < min_height or img.width < min_width:
            raise ValidationError('The resolution of the uploaded image is less than the minimum allowed')
        if img.height > max_height or img.width > max_width:
            new_img = img.convert('RGB')
            resized_new_image = new_img.resize((800, 800), Image.ANTIALIAS)
            filestream = BytesIO()
            resized_new_image.save(filestream, 'JPEG', quality=90)
            filestream.seek(0)
            self.image = InMemoryUploadedFile(
                filestream, 'ImageField', self.image.name, 'jpeg/image', sys.getsizeof(filestream), None
            )
        super().save(*args, **kwargs)


class CartProduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name='Customer', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='cart product', on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    amount = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Total_price')

    def __str__(self):
        return f'Product: {self.product.title} (in the cart)'


class Cart(models.Model):
    owner = models.ForeignKey('Customer', verbose_name='owner of the cart', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    products_amount = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Total_price')

    def __str__(self):
        return self.pk


class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name='Customer', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Phone number')
    address = models.CharField(max_length=255, verbose_name='Address')

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
    sd = models.BooleanField(default=True)
    sd_memory_max = models.CharField(max_length=255, verbose_name='Maximum memory capacity')
    main_cam_mp = models.CharField(max_length=255, verbose_name='Main camera')
    front_cam_mp = models.CharField(max_length=255, verbose_name='Front camera')

    def __str__(self):
        return f'{self.category.name} : {self.title}'

