from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from .forms import RegisterForm, LoginForm
from .models import CustomUser
from django.contrib.auth.decorators import login_required  # Import CustomUser explicitly

def registerPage(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()  # Save user
            return redirect('login')  # Redirect to login page
    else:
        form = RegisterForm()
    return render(request, 'finance/register.html', {'form': form})

def loginPage(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            # Authenticate with 'username' as email
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                form.add_error(None, "Invalid email or password.")
    else:
        form = LoginForm()
    return render(request, 'finance/login.html', {'form': form})

def logoutPage(request):
    logout(request)
    return redirect('login')
@login_required(login_url='login')  # Redirects to login if user is not authenticated
def home(request):
    return render(request, 'finance/home.html')

@login_required(login_url='login')
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        logout(request)  # Log out the user before deletion
        user.delete()  # Delete the user
        return redirect('login')  # Redirect to login page after deletion