from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser, Transaction, Category, SubCategory, UserCategory, BankBalance

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
        fields = ['username', 'email', 'password1', 'password2', 'user_category']
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
            'email': None,
        }

class LoginForm(forms.Form):
    username_or_email = forms.CharField(
        label="Username or Email",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['subcat', 't_description', 'amount', 'custom', 't_date']
        widgets = {
            't_date': forms.DateInput(attrs={'type': 'date'}),
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TransactionForm, self).__init__(*args, **kwargs)
        
        if user:
            # Filter subcategories based on user's categories
            user_categories = UserCategory.objects.filter(user=user)
            categories = Category.objects.filter(user_cat__in=user_categories)
            self.fields['subcat'].queryset = SubCategory.objects.filter(category__in=categories)

class CustomCategoryForm(forms.ModelForm):
    subcat_name = forms.CharField(
        label='Custom Category Name',
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your custom category name',
            'class': 'form-control'
        })
    )

    class Meta:
        model = SubCategory
        fields = ['subcat_name']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CustomCategoryForm, self).__init__(*args, **kwargs)

    def clean_subcat_name(self):
        name = self.cleaned_data['subcat_name']
        
        # Check if category already exists for this user
        if SubCategory.objects.filter(
            category__user_cat__user=self.user,
            subcat_name__iexact=name
        ).exists():
            raise ValidationError('This category already exists.')
        
        # Validate length
        if len(name) < 3:
            raise ValidationError('Category name must be at least 3 characters long.')
        
        return name

class BankBalanceForm(forms.ModelForm):
    class Meta:
        model = BankBalance
        fields = ['balance']
        widgets = {
            'balance': forms.NumberInput(attrs={
                'step': '0.01',
                'class': 'form-control'
            })
        }
