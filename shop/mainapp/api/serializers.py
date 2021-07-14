from rest_framework import serializers

from ..models import Category, Customer, Order, Product


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True)

    class Meta:
        model = Customer
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

