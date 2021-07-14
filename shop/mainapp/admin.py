from django.forms import ModelChoiceField, ModelForm
from django.contrib import admin
from django.utils.html import format_html
from django.utils.http import urlencode
from django.utils.safestring import mark_safe

from .models import *
from .mixins import ImageValidationMixin


class OrdersAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'cart', 'status', 'buying_type', 'comment', 'order_creation_date', 'order_completion_date')
    list_filter = ('status', 'customer')
    search_fields = ('customer',)


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'products_amount', 'total_price', 'get_products')
    list_filter = ('owner',)
    search_fields = ('owner', 'id')

    def get_products(self, obj):
        return obj.products.all()


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone')


admin.site.register(Category)
admin.site.register(CartProduct)
admin.site.register(Cart, CartAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrdersAdmin)
admin.site.register(Product)


