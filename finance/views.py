#hi this is sandy
#new change made by prajwal
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from .forms import registerform, loginform
from django.contrib.auth.models import User

def registerPage(request):
    if request.method == 'POST':
        form.registerform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('loginPage')
    else:
        form=registerform()
    return render(request,'finance/register.html',{'form':form})

def loginPage(request):
    if request.method=='POST':
        form=loginform(request.POST)
        if form.is_valid():
            email= form.cleaned_data.get('email')
            password= form.cleaned_data.get('password')
            try:
                user=User.objects.get(email=email)
                user = authenticate(request,email=email,password=password)
                if user is not None:
                    login(request,user)
                    return redirect('home')
                else:
                    form.add_error(None, "Invalid email or password.")
            except User.DoesNotExist:
                form.add_error(None, "User with this email does not exist.")
    else:
            form=loginform()
    return render(request,'finance/login.html',{'form':form})
    def user_logout(request):
        logout(request)
        return redirect('loginPage')
    



