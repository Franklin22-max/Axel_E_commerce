from pyexpat import model
from django.contrib.auth.forms import UserCreationForm
from .models import Product
from django import forms

class productCreationForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['owner','name','price','description','quantity','genre','brand']