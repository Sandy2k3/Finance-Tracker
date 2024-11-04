from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login ,logout 
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required 
from django.conf import settings
from .forms import RegisterForm, LoginForm

def registerPage(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after registration
    else:
        form = RegisterForm()  # Empty form for GET requests
    return render(request, 'finance/register.html', {'form': form})

def loginPage(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            try:
                # Fetch user by email
                user = User.objects.get(email=email)

                # Authenticate using the username (since we fetched the user by email)
                user = authenticate(request, username=user.username, password=password)

                if user is not None:
                    login(request, user)  # Log the user in
                    return redirect(settings.LOGIN_REDIRECT_URL)  # Redirect to home
                else:
                    form.add_error(None, "Invalid email or password.")
            except User.DoesNotExist:
                form.add_error(None, "User with this email does not exist.")
    else:
        form = LoginForm()  # Display an empty form for GET requests

    return render(request, 'finance/login.html', {'form': form})

@login_required(login_url='home')
def home(request):
    return render(request, 'finance/home.html')

def logoutPage(request):
    logout(request)  # Log the user out
    return redirect('login')