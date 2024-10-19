from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User  # Correct import for the User model
from .forms import *
def index(request):
    return render(request, 'index.html')

def registerPage(request):
    if request.method == 'POST':
        form=registerform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form=registerform()
    return render(request,'finance/register.html',{'form':form})
def loginPage(request):
    if request.method == 'POST':
        form = loginform(request.POST)
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
                    return redirect('home')  # Redirect after login
                else:
                    form.add_error(None, "Invalid email or password.")
            except User.DoesNotExist:
                form.add_error(None, "User with this email does not exist.")
    else:
        form = loginform()  # Display an empty form for GET requests

    return render(request, 'finance/login.html', {'form': form})
