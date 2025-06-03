from django.db import models
from users.models import User, DriverProfile


from django.db import models
from users.models import User

class Ride(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    rider = models.ForeignKey(User, related_name='rides', on_delete=models.CASCADE)
    driver = models.ForeignKey(User, related_name='driver_rides', on_delete=models.SET_NULL, null=True, blank=True)
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    fare_estimate = models.FloatField(null=True, blank=True)  # optional for now

    def __str__(self):
        return f"Ride from {self.pickup_location} to {self.dropoff_location} by {self.rider.user_name}"
