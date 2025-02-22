from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('home/', views.home, name='home'),
    path('logout/', views.logoutPage, name='logout'),
    path('delete_user/', views.delete_user, name='delete_user'),
    path('profile/', views.profile_view, name='profile'),
    path('add_transaction/', views.add_transaction, name='add_transaction'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('categories/', views.category_list, name='category_list'),
    path('perform_analysis/', views.perform_analysis, name='perform_analysis'),
    path('generate_report/', views.generate_report, name='generate_report'),
    
    # API endpoints
    path('api/get_subcategories/', views.get_subcategories, name='get_subcategories'),
    path('api/monthly-data/', views.get_monthly_data, name='get_monthly_data'),
    path('api/monthly-breakdown/', views.get_monthly_breakdown, name='get_monthly_breakdown'),
    
    # Other URLs
    path('delete-transaction/<int:t_id>/', views.delete_transaction, name='delete_transaction'),
    path('update-balance/', views.update_balance, name='update_balance'),
]