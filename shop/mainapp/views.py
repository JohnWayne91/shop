import stripe

from django.contrib.auth import login
from django.db import transaction
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import DetailView, View, CreateView, ListView, TemplateView
from django.contrib.auth.views import LoginView

from .models import *
from .mixins import CartMixin, GetCartProductMixin, DataMixin
from .forms import OrderForm, SignInUserForm, RegisterUserForm
from .utils import recalculate_cart


class BaseView(DataMixin, ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'base.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_context(title='Home')
        all_context = context | user_context
        return all_context

    def get_queryset(self):
        return Product.objects.all().order_by('-id')


class ProductDetailView(DataMixin, DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_context(title='Product detail')
        all_context = context | user_context
        return all_context


class CategoryDetailView(DataMixin, ListView):
    model = Category
    queryset = Category.objects.all()
    context_object_name = 'categories'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_context(
            title='Category - ' + str(self.kwargs['slug']),
            category_products=Product.objects.filter(category__slug=self.kwargs['slug']).order_by('-id')
        )
        all_context = context | user_context
        return all_context


class AddToCartView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/sign-in/')
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, product=product
        )
        if created:
            self.cart.products.add(cart_product)
        recalculate_cart(self.cart)
        messages.add_message(request, messages.INFO, 'Product added to cart successfully')
        return HttpResponseRedirect('/cart/')


class DeleteFromCartView(CartMixin, GetCartProductMixin, View):

    def get(self, request, *args, **kwargs):
        cart_product = self.cart_product
        self.cart.products.remove(cart_product)
        cart_product.delete()
        recalculate_cart(self.cart)
        messages.add_message(request, messages.INFO, 'Product deleted successfully')
        return HttpResponseRedirect('/cart/')


class ChangeProductAmountView(CartMixin, GetCartProductMixin, View):
    def post(self, request, *args, **kwargs):
        cart_product = self.cart_product
        amount = int(request.POST.get('amount'))
        cart_product.amount = amount
        cart_product.save()
        recalculate_cart(self.cart)
        messages.add_message(request, messages.INFO, 'Product amount changed successfully')
        return HttpResponseRedirect('/cart/')


class CartView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {
            'categories': categories,
            'cart': self.cart,
            'title': 'Cart'
        }
        return render(request, 'cart.html', context)


class CheckoutView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        stripe.api_key = "sk_test_51J5qylB2DXIlYuJKR86lqr5k2sRhIgION88pWjV0Wtbb7AnoV7jOHqUoXf4WKR9IZa9I7dy2Wkx0ZAFXY9w6rekm00DaZJ6Zp5"

        intent = stripe.PaymentIntent.create(
            amount=int(self.cart.total_price * 100),
            currency='usd',
            # Verify your integration in this guide by including this parameter
            metadata={'integration_check': 'accept_a_payment'},
        )
        categories = Category.objects.all()
        form = OrderForm(request.POST or None)
        context = {
            'categories': categories,
            'cart': self.cart,
            'form': form,
            'client_secret': intent.client_secret
        }
        return render(request, 'checkout.html', context)


class MakeOrderView(CartMixin, View):
    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.buying_type = form.cleaned_data['buying_type']
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            customer.orders.add(new_order)
            messages.add_message(request, messages.INFO, 'New order created successfully, manager will contact you soon')
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/checkout/')


class PayedOnlineOrderView(CartMixin, View):
    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        new_order = Order()
        new_order.customer = customer
        new_order.first_name = customer.user.first_name
        new_order.last_name = customer.user.last_name
        new_order.phone = customer.phone
        new_order.address = customer.address
        new_order.buying_type = Order.BUYING_TYPE_SELF
        self.cart.in_order = True
        self.cart.save()
        new_order.cart = self.cart
        new_order.status = Order.STATUS_PAYED
        new_order.save()
        customer.orders.add(new_order)
        return JsonResponse({"status": "payed"})


class SignInUser(DataMixin, LoginView):
    form_class = SignInUserForm
    template_name = 'sign_in.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_context(title='Sign_in')
        all_context = context | user_context
        return all_context

    def get_success_url(self):
        return reverse_lazy('base')


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'sign_up.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_context(title='Sign_up')
        all_context = context | user_context
        return all_context

    def form_valid(self, form):
        user = form.save()
        Customer.objects.create(
            user=user,
            phone=form.cleaned_data['phone'],
            address=form.cleaned_data['address']
        )
        login(self.request, user)
        return redirect('base')


class ProfileView(DataMixin, TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = Customer.objects.get(user=self.request.user)
        user_context = self.get_context(
            title='Profile',
            orders=Order.objects.filter(customer=customer).order_by('-order_creation_date')
        )
        all_context = context | user_context
        return all_context











