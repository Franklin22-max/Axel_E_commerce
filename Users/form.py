from pyexpat import model
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms

class signinForm(UserCreationForm):
    email = forms.EmailField()
    phone = forms.IntegerField()
    gender = forms.CharField()
    
    class Meta:
        model = User
        fields = ['username', 'email','phone','gender', 'password1', 'password2']

class passResetForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['email']

"""class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email']
"""