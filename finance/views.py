from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.urls import reverse_lazy
from .forms import RegisterForm, LoginForm
from .models import CustomUser ,UserCategory, Category, SubCategory, Transaction, BankBalance
from django.contrib.auth.decorators import login_required  # Import CustomUser explicitly
from .forms import TransactionForm
from .forms import CustomCategoryForm
from django.contrib import messages
from django.http import JsonResponse
from .forms import BankBalanceForm
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.utils.decorators import method_decorator

def registerPage(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create initial bank balance with 0
            BankBalance.objects.create(
                user=user,
                balance=0
            )
            
            # Create UserCategory
            user_category = UserCategory.objects.create(
                user=user,
                user_category=user.user_category
            )
            
            # Define categories based on user type
            if user.user_category == 'business':
                categories_data = {
                    'Income': [
                        'Sales Revenue', 'Consulting Fees', 'Product Sales', 
                        'Service Income', 'Investment Returns', 'Rental Income',
                        'Grants/Subsidies', 'Interest Income', 'Licensing Fees',
                        'Franchise Income', 'Partnership Earnings'
                    ],
                    'Expenses': [
                        'Salaries/Wages', 'Rent/Lease', 'Utilities', 
                        'Supplies/Inventory', 'Marketing/Advertising', 'Insurance',
                        'Legal Fees', 'Travel', 'Office Equipment', 
                        'Loan Repayments', 'Taxes', 'Professional Services',
                        'R&D', 'Employee Benefits', 'Training/Development',
                        'Maintenance'
                    ]
                }
            else:  # personal
                categories_data = {
                    'Income': [
                        'Salary/Wages', 'Investments', 'Freelance/Side Jobs',
                        'Gifts/Donations', 'Rental Income', 'Interest/Dividends',
                        'Government Benefits', 'Reimbursements'
                    ],
                    'Expenses': [
                        'Food/Groceries', 'Rent/Mortgage', 'Utilities',
                        'Transportation', 'Healthcare/Medical', 'Education',
                        'Entertainment', 'Clothing', 'Insurance', 
                        'Personal Loans', 'Savings/Investments', 'Gifts/Charity'
                    ]
                }
            
            try:
                # Create categories and subcategories
                for cat_name, subcats in categories_data.items():
                    # Create category
                    category = Category.objects.create(
                        user_cat=user_category,
                        cat_name=cat_name
                    )
                    print(f"Created category: {category}")
                    
                    # Create subcategories
                    for subcat_name in subcats:
                        subcategory = SubCategory.objects.create(
                            category=category,
                            subcat_name=subcat_name
                        )
                        print(f"Created subcategory: {subcategory}")
                
                # Create Custom category
                custom_category = Category.objects.create(
                    user_cat=user_category,
                    cat_name='Custom'
                )
                print(f"Created custom category: {custom_category}")
                
            except Exception as e:
                print(f"Error creating categories: {str(e)}")
                
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'finance/register.html', {'form': form})

@ensure_csrf_cookie
@csrf_protect
def loginPage(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username_or_email')
            password = form.cleaned_data.get('password')
            
            user = authenticate(email=email, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('home')
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
    try:
        bank_balance = request.user.bank_balance
    except BankBalance.DoesNotExist:
        bank_balance = BankBalance.objects.create(user=request.user, balance=0)
    
    context = {
        'bank_balance': bank_balance,
    }
    return render(request, 'finance/home.html', context)

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
    if request.method == 'POST':
        category_type = request.POST.get('category')
        
        if category_type == 'Custom':
            try:
                # Get the custom subcategory name from the input field
                custom_subcat_name = request.POST.get('subcat')
                
                # Get the user's custom category
                custom_category = Category.objects.get(
                    user_cat__user=request.user,
                    cat_name='Custom'
                )
                
                # Create or get the subcategory
                subcategory, created = SubCategory.objects.get_or_create(
                    category=custom_category,
                    subcat_name=custom_subcat_name
                )
                
                # Create the transaction
                Transaction.objects.create(
                    user=request.user,
                    subcat=subcategory,
                    t_description=request.POST.get('t_description'),
                    amount=request.POST.get('amount'),
                    custom=request.POST.get('custom'),
                    t_date=request.POST.get('t_date')
                )
                
                print(f"Transaction created with custom subcategory: {custom_subcat_name}")
                return redirect('transaction_list')
                
            except Exception as e:
                print(f"Error creating custom transaction: {str(e)}")
                form = TransactionForm(request.POST, user=request.user)
                
        else:
            # Handle regular categories (Income/Expenses)
            form = TransactionForm(request.POST, user=request.user)
            if form.is_valid():
                try:
                    transaction = form.save(commit=False)
                    transaction.user = request.user
                    transaction.save()
                    print(f"Transaction created with regular category")
                    return redirect('transaction_list')
                except Exception as e:
                    print(f"Error creating regular transaction: {str(e)}")
    else:
        form = TransactionForm(user=request.user)
    
    return render(request, 'finance/add_transaction.html', {'form': form})


@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user)  # Filter by user
    return render(request, "finance/transaction_list.html", {"transactions": transactions})

@login_required
def category_list(request):
    categories = Category.objects.filter(user_cat__user=request.user)  # Filter by user category
    return render(request, "finance/category_list.html", {"categories": categories})


@login_required
def perform_analysis(request):
    return render(request, 'finance/perform_analysis.html', {'message': 'Performing analysis... this will be where the analysis happens!'})

@login_required
def generate_report(request):
    return render(request, 'finance/generate_report.html', {'message': 'Generating report... this will be where the report generation happens!'})

@login_required
def get_subcategories(request):
    category = request.GET.get('category')
    user = request.user
    
    # Debug prints
    print(f"User: {user.username}")
    print(f"Selected category: {category}")
    
    # Get user categories
    user_categories = UserCategory.objects.filter(user=user)
    print(f"User categories: {user_categories}")
    
    # Get the category object
    categories = Category.objects.filter(
        user_cat__in=user_categories,
        cat_name=category
    )
    print(f"Found categories: {categories}")
    
    # Get subcategories
    subcategories = SubCategory.objects.filter(
        category__in=categories
    ).values('id', 'subcat_name')
    
    subcategories_list = list(subcategories)
    print(f"Subcategories: {subcategories_list}")
    
    return JsonResponse(subcategories_list, safe=False)

@login_required
def delete_transaction(request, t_id):
    # Get the transaction
    transaction = get_object_or_404(Transaction, t_id=t_id, user=request.user)
    
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Transaction deleted successfully!')
        return redirect('transaction_list')
    
    return render(request, 'finance/delete_transaction.html', {'transaction': transaction})

@login_required
def update_balance(request):
    try:
        bank_balance = BankBalance.objects.get(user=request.user)
    except BankBalance.DoesNotExist:
        bank_balance = BankBalance.objects.create(user=request.user, balance=0)

    if request.method == 'POST':
        form = BankBalanceForm(request.POST, instance=bank_balance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bank balance updated successfully!')
            return redirect('home')
    else:
        form = BankBalanceForm(instance=bank_balance)

    return render(request, 'finance/update_balance.html', {'form': form})
