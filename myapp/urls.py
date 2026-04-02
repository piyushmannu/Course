# myapp/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('category/',enter_category),
]