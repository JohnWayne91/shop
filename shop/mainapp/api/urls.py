from django.urls import path

from .api_views import CategoryListCreateApiView, SmartphoneListApiView, NotebookListApiView, SmartphoneDetailApiView, \
    CustomerListApiView, CategoryDetailApiView


urlpatterns = [
    path('categories/', CategoryListCreateApiView.as_view(), name='categories'),
    path('categories/<str:id>/', CategoryDetailApiView.as_view(), name='categories_detail'),
    path('customers/', CustomerListApiView.as_view(), name='customers'),
    path('smartphones/', SmartphoneListApiView.as_view(), name='smartphones'),
    path('notebooks/', NotebookListApiView.as_view(), name='notebooks'),
    path('smartphones/<str:id>/', SmartphoneDetailApiView.as_view(), name='smartphone_detail'),
    path('notebooks/<str:id>/', SmartphoneDetailApiView.as_view(), name='smartphone_detail')
]
