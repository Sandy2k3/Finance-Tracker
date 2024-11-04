from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
        help_text='',
    )
    password2 = forms.CharField(
        label="Confirm Password",
        strip=False,
        widget=forms.PasswordInput,
        help_text='',
    )
    user_category = forms.ChoiceField(
        label="User Category",
        choices=[
            ('business', 'Business'),
            ('personal', 'Personal'),
        ],
        required=True
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
            'email': None,
            'user_category':None
        }

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=254, required=True)
    password = forms.CharField(max_length=128, required=True, widget=forms.PasswordInput)
