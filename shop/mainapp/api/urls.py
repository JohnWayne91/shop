from django.urls import path

from .api_views import CategoryListCreateApiView, CustomerListApiView, CategoryDetailApiView


urlpatterns = [
    path('categories/', CategoryListCreateApiView.as_view(), name='categories'),
    path('categories/<str:id>/', CategoryDetailApiView.as_view(), name='categories_detail'),
    path('customers/', CustomerListApiView.as_view(), name='customers'),
]
