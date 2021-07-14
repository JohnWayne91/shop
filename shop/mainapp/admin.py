from django.contrib import admin

from .models import *


class OrdersAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'cart', 'status', 'buying_type', 'comment', 'order_creation_date', 'order_completion_date')
    list_filter = ('status', 'customer')
    search_fields = ('id',)


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'products_amount', 'total_price', 'get_products')
    list_filter = ('owner',)
    search_fields = ('owner', 'id')

    def get_products(self, obj):
        return obj.products.all()


class ProductAmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'category')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('category',)
    search_fields = ('id', 'title')


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone')


admin.site.register(Category)
admin.site.register(CartProduct)
admin.site.register(Cart, CartAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrdersAdmin)
admin.site.register(Product, ProductAmin)


