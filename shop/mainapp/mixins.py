from PIL import Image

from django.forms import ValidationError
from django.views.generic import View

from .models import Product, Customer, Cart, CartProduct, Category


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


class CartMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = Customer.objects.filter(user=request.user).first()
            if not customer:
                customer = Customer.objects.create(user=request.user)
            cart = Cart.objects.filter(owner=customer, in_order=False).first()
            if not cart:
                cart = Cart.objects.create(owner=customer)
        else:
            cart = Cart.objects.filter(for_anonymous_user=True).first()
            if not cart:
                cart = Cart.objects.create(for_anonymous_user=True)
        self.cart = cart
        return super().dispatch(request, *args, **kwargs)


class GetCartProductMixin(View):
    def dispatch(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        self.cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product
        )
        return super().dispatch(request, *args, **kwargs)


class DataMixin(CartMixin):
    paginate_by = 6

    def get_context(self, **kwargs):
        context = kwargs
        categories = Category.objects.all()
        context['categories'] = categories
        context['cart'] = self.cart
        return context

