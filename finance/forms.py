from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class registerform(UserCreationForm):
        password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
        help_text='',  # Remove help text
    )
        password2 = forms.CharField(
        label="Confirm Password",
        strip=False,
        widget=forms.PasswordInput,
        help_text='',  # Remove help text
    )

class Meta:
        model=User
        fields=['first_name','last_name','username','email','password1','password2']
        help_texts = {
            'username': None,  # Remove help text for username
            'password1': None,  # Remove help text for password
            'password2': None,
            'email':None,    # Remove help text for password confirmation
        }

class loginform(forms.Form):
    email= forms.EmailField(max_length=254,required=True)
    password=forms.CharField(max_length=128,required=True,widget=forms.PasswordInput)