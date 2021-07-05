from django import forms

from mainapp.models import Category
from .models import CategorySpecification


class NewCategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = '__all__'


class NewCategorySpecKeyForm(forms.ModelForm):
    class Meta:
        model = CategorySpecification
        fields = '__all__'
