import sys
from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models


def recalculate_cart(cart):
    cart_data = cart.products.aggregate(models.Sum('total_price'), models.Count('id'))
    if cart_data.get('total_price__sum'):
        cart.total_price = cart_data['total_price__sum']
    else:
        cart.total_price = 0
    cart.products_amount = cart_data['id__count']
    cart.save()


def resize_image(self, *args, **kwargs):
    image = self.image
    img = Image.open(image)
    max_height, max_width = self.MAX_RESOLUTION
    if img.height > max_height or img.width > max_width:
        new_img = img.convert('RGB')
        resized_new_image = new_img.resize((800, 800), Image.ANTIALIAS)
        filestream = BytesIO()
        resized_new_image.save(filestream, 'JPEG', quality=90)
        filestream.seek(0)
        self.image = InMemoryUploadedFile(
            filestream, 'ImageField', self.image.name, 'jpeg/image', sys.getsizeof(filestream), None
        )