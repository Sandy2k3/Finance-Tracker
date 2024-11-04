from . import views
from django.urls import path,include

urlpatterns = [
    path('login/',views.loginPage,name='login'),
    path('register/',views.registerPage,name='register'),
    path('home/',views.home,name='home'),
    path('logout/',views.logoutPage,name='logout'),
    path('delete_user/', views.delete_user, name='delete_user'),
]