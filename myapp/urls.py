from django.urls import path
from .views import *

urlpatterns = [
    path('category/',category_section),
]