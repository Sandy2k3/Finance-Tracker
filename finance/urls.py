from . views import *
from django.urls import path,include

urlpatterns = [
    path('registerPage/',registerPage,name='registerPage'),
    path('loginPage/',loginPage,name='loginPage')
]