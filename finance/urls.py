from . import hello
from django.urls import path,include

urlpatterns = [
    path('hello/',hello,name='hello'),
]