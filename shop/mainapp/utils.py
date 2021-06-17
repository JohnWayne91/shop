from PIL import Image
from django.forms import ValidationError
from django.views.generic.detail import SingleObjectMixin
from .models import Product, Category, Customer, Cart1


class ImageValidationMixin:
    def validate_image(self):
        image = self.cleaned_data['image']
        img = Image.open(image)
        min_height, min_width = Product.MIN_RESOLUTION
        if image.size > Product.MAX_IMAGE_SIZE:
            raise ValidationError('The size of the uploaded image is more than 3 MB')
        if img.height < min_height or img.width < min_width:
            raise ValidationError('The resolution of the uploaded image is less than the minimum allowed')
        return image


class GetCustomerCartMixin:
    def get_cart(self):
        customer = Customer.objects.get(user=self.request.user)
        cart = Cart1.objects.get(owner=customer, in_order=False)
        return cart


class CategoryDetailMixin(SingleObjectMixin, GetCustomerCartMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.get_categories_for_left_sidebar()
        cart = self.get_cart()
        context['cart'] = cart
        return context




