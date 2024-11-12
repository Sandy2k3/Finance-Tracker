from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.urls import reverse_lazy
from .forms import RegisterForm, LoginForm
from .models import CustomUser ,UserCategory, Category, SubCategory, Transaction
from django.contrib.auth.decorators import login_required  # Import CustomUser explicitly
from .forms import TransactionForm

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
   
@login_required
def profile_view(request):
    # Pass the user info to the template
    return render(request, 'finance/profile.html', {'user': request.user})

@login_required
def add_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect("home")  # Redirect to home or another page after saving
    else:
        form = TransactionForm()
    return render(request, "finance/add_transaction.html", {"form": form})

@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user)
    return render(request, "finance/transaction_list.html", {"transactions": transactions})

@login_required
def category_list(request):
    categories = Category.objects.filter(user_cat__user=request.user)
    return render(request, "finance/category_list.html", {"categories": categories})

@login_required
def perform_analysis(request):
    return render(request, 'finance/perform_analysis.html', {'message': 'Performing analysis... this will be where the analysis happens!'})

@login_required
def generate_report(request):
    return render(request, 'finance/generate_report.html', {'message': 'Generating report... this will be where the report generation happens!'})
