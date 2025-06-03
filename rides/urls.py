app_name = 'rides'
from django.urls import path
from .views import BookRideView, AvailableRidesView, AcceptRideView, UserRideHistoryView


urlpatterns = [
    path('book', BookRideView.as_view(), name='book_ride'),
    path('available', AvailableRidesView.as_view(), name='available_rides'),
    path('accept/<int:ride_id>/', AcceptRideView.as_view(), name='accept_ride'),
    path('myrides/', UserRideHistoryView.as_view(), name='user_ride_history'),
]
