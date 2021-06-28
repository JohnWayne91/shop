from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Order


class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order_completion_date'].label = 'Date of receipt of the order'

    order_completion_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'phone', 'address', 'buying_type', 'order_completion_date', 'comment')


class SignInUserForm(AuthenticationForm):
    username = forms.CharField(label='Login')
    password = forms.CharField(label='Password')