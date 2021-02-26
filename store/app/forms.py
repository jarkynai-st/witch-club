from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Order




class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['product','user','payment_type']


class SignupForm(UserCreationForm):
    email = forms.EmailField

    class Meta:
        model = User
        fields = ['username','email','password1','password2']


