from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.filters import SearchFilter

from .serializers import CategorySerializers, SmartphoneSerializer, NotebookSerializer, CustomerSerializer
from ..models import Category, Smartphone, Notebook, Customer


class CategoryListApiView(ListAPIView):

    serializer_class = CategorySerializers
    queryset = Category.objects.all()


class SmartphoneListApiView(ListAPIView):

    serializer_class = SmartphoneSerializer
    queryset = Smartphone.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['price', 'title']


class NotebookListApiView(ListAPIView):

    serializer_class = NotebookSerializer
    queryset = Notebook.objects.all()


class SmartphoneDetailApiView(RetrieveAPIView):

    serializer_class = SmartphoneSerializer
    queryset = Smartphone.objects.all()
    lookup_field = 'id'


class NotebookDetailApiView(RetrieveAPIView):

    serializer_class = NotebookSerializer
    queryset = Notebook.objects.all()
    lookup_field = 'id'


class CustomerListApiView(ListAPIView):

    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()