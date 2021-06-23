from django.urls import path

from .api_views import CategoryListApiView


urlpatterns = [
    path('categories/', CategoryListApiView.as_view(), name='categories')
]