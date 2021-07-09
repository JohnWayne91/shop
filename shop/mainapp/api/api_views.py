from collections import OrderedDict

from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .serializers import *
from ..models import Category, Customer


class ProductPagination(PageNumberPagination):

    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 10

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('products_count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('products', data)
        ]))


class CategoryListCreateApiView(ListCreateAPIView):

    serializer_class = CategorySerializers
    queryset = Category.objects.all()


class CategoryDetailApiView(RetrieveAPIView, RetrieveUpdateAPIView):

    serializer_class = CategorySerializers
    queryset = Category.objects.all()
    lookup_field = 'id'


class CustomerListApiView(ListAPIView):

    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()


class ProductDetailApiView(RetrieveAPIView, RetrieveUpdateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = 'id'


class AllProductsListApiView(ListAPIView, ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by("-id")
    pagination_class = ProductPagination
    filter_backends = [SearchFilter]
    search_fields = ['price', 'title']


class NotebooksListApiView(ListAPIView, ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(category="1").order_by("-id")
    pagination_class = ProductPagination
    filter_backends = [SearchFilter]
    search_fields = ['price', 'title']


class SmartphoneListApiView(ListAPIView, ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(category="2").order_by("-id")
    pagination_class = ProductPagination
    filter_backends = [SearchFilter]
    search_fields = ['price', 'title']