from django.urls import path

from .views import BaseSpecView, CreateNewCategory, CreateNewSpec

urlpatterns = [
    path('', BaseSpecView.as_view(), name='base_spec'),
    path('new-category/', CreateNewCategory.as_view(), name='new_category'),
    path('new-specification/', CreateNewSpec.as_view(), name='new_spec')
]
