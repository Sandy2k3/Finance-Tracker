from . import views
from django.urls import path,include

urlpatterns = [
    path('login/',views.loginPage,name='login'),
    path('register/',views.registerPage,name='register'),
]