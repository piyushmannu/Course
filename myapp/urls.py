from django.urls import path
from .views import *

urlpatterns = [
    # List all categories & create new
    path('category/', enter_category, name='category-list-create'),
    path('course/', enter_course),
    
    # Get single category, update, delete
    # path('category/<int:category_id>/', get_category_detail, name='category-detail'),
]