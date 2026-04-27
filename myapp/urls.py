from django.urls import path
from .views import *

urlpatterns = [
    # List all categories & create new
    path('category/', enter_category, name='category-list-create'),
    path('course/', enter_course),
    path('lesson/',enter_lesson),
    path('enrollment/',enrollment_status),
    path('coupon/',coupon_status),
    path('payment/',payment_status),
    path('review/',review_posting),

    
    # Get single category, update, delete
    # path('category/<int:category_id>/', get_category_detail, name='category-detail'),
]