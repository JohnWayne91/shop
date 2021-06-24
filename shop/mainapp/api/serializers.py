from rest_framework import serializers

from ..models import Category, Smartphone, Notebook, Customer, Order


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class SmartphoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Smartphone
        fields = '__all__'


class NotebookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notebook
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):

    orders = OrderSerializer(many=True)

    class Meta:
        model = Customer
        fields = '__all__'

