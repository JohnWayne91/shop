from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import View, CreateView
from django.http import HttpResponseRedirect

from .forms import NewCategoryForm, NewCategorySpecKeyForm


class BaseSpecView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'product_specifications.html', {})


class CreateNewCategory(CreateView):

    form_class = NewCategoryForm
    template_name = 'new_category.html'
    success_url = reverse_lazy('base_spec')


class CreateNewSpec(CreateView):
    form_class = NewCategorySpecKeyForm
    template_name = 'new_specification.html'
    success_url = reverse_lazy('base_spec')
