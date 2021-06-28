from django.forms import ModelChoiceField, ModelForm
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *
from .mixins import ImageValidationMixin


admin.site.register(Category)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Product)


