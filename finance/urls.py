from . import views
from django.urls import path,include

urlpatterns = [
    path('login/',views.loginPage,name='login'),
    path('register/',views.registerPage,name='register'),
    path('home/',views.home,name='home'),
    path('logout/',views.logoutPage,name='logout'),
    path('delete_user/', views.delete_user, name='delete_user'),
    path('profile/', views.profile_view, name='profile'),
    path("add_transaction/", views.add_transaction, name="add_transaction"),
    path("transactions/", views.transaction_list, name="transaction_list"),
    path("categories/", views.category_list, name="category_list"),
    path('perform_analysis/', views.perform_analysis, name='perform_analysis'),
    path('generate_report/', views.generate_report, name='generate_report'),
    path('get_subcategories/', views.get_subcategories, name='get_subcategories'),
]