from django.urls import path

from .api_views import CategoryListCreateApiView, CustomerListApiView, CategoryDetailApiView, ProductDetailApiView,\
    AllProductsListApiView, NotebooksListApiView, SmartphoneListApiView


urlpatterns = [
    path('categories/', CategoryListCreateApiView.as_view(), name='categories'),
    path('categories/<str:id>/', CategoryDetailApiView.as_view(), name='categories_detail'),
    path('customers/', CustomerListApiView.as_view(), name='customers'),
    path('product/<str:id>/', ProductDetailApiView.as_view(), name='product'),
    path('all-products/', AllProductsListApiView.as_view(), name='all_products'),
    path('notebooks/', NotebooksListApiView.as_view(), name='notebooks'),
    path('smartphones/', SmartphoneListApiView.as_view(), name='smartphones')
]
