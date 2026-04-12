from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

urlpatterns = [
    path('category/',enter_category),
    path('hello/',Helloview.as_view()),
    path('auth/register/', register),
    path('auth/refresh/',  TokenRefreshView.as_view()),  # simplejwt handles this

]
