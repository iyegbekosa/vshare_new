app_name = 'users'

from django.urls import path
from .views import CustomUserCreate, CustomDriverCreate, RiderLoginView, DriverLoginView

urlpatterns = [
    path('register_user', CustomUserCreate.as_view(), name='register_user'),
    path('register_driver', CustomDriverCreate.as_view(), name='register_driver'),
    path('login_user', RiderLoginView.as_view(), name='login_user'),
    path('login_driver', DriverLoginView.as_view(), name='login_driver'),
]