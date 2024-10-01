from . import hel
from django.urls import path,include

urlpatterns = [
    path('hello/',hello,name='hello'),
]