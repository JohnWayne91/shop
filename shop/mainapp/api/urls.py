from django.urls import path

from .api_views import CategoryListApiView, SmartphoneListApiView, NotebookListApiView, SmartphoneDetailApiView, \
    CustomerListApiView


urlpatterns = [
    path('categories/', CategoryListApiView.as_view(), name='categories'),
    path('customers/', CustomerListApiView.as_view(), name='customers'),
    path('smartphones/', SmartphoneListApiView.as_view(), name='smartphones'),
    path('notebooks/', NotebookListApiView.as_view(), name='notebooks'),
    path('smartphones/<str:id>/', SmartphoneDetailApiView.as_view(), name='smartphone_detail'),
    path('notebooks/<str:id>/', SmartphoneDetailApiView.as_view(), name='smartphone_detail')
]
