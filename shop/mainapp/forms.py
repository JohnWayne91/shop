from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

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


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Login')
    first_name = forms.CharField(label='First name')
    last_name = forms.CharField(label='Last name')
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password')
    password2 = forms.CharField(label='Repeat password')
    address = forms.CharField(label='Address')
    phone = forms.CharField(label='Phone number')
    # captcha = CaptchaField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'address', 'phone']
