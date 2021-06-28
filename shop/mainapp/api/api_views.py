from collections import OrderedDict

from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .serializers import CategorySerializers, CustomerSerializer
from ..models import Category, Customer


class ProductPagination(PageNumberPagination):

    page_size = 2
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