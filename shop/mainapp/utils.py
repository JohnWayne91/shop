from django.db import models


def recalculate_cart(cart):
    cart_data = cart.products.aggregate(models.Sum('total_price'), models.Count('id'))
    if cart_data.get('total_price__sum'):
        cart.total_price = cart_data['total_price__sum']
    else:
        cart.total_price = 0
    cart.products_amount = cart_data['id__count']
    cart.save()