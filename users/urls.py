app_name = 'users'

from django.urls import path
from .views import CustomUserCreate, CustomDriverCreate

urlpatterns = [
    path('register_user', CustomUserCreate.as_view(), name='register_user'),
    path('register_driver', CustomDriverCreate.as_view(), name='register_driver'),
]
