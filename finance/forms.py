from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class registerform(UserCreationForm):
    class Meta:
        model=User
        fields=['email','password1','password2']

class loginform(forms.Form):
    email= forms.EmailField(max_length=254,required=True)
    password=forms.CharField(max_length=128,required=True,widget=forms.PasswordInput)