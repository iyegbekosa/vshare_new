from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomAccountManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password, **other_fields):
        
        if not email:
            raise ValueError(_('You must provide a valid email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **other_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, first_name, last_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('role', 'admin')

        if other_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must be assigned is_staff=True'))
        
        if other_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must be assigned is_superuser=True'))
        
        return self.create_user(email, first_name, last_name, password, **other_fields)



class User(AbstractBaseUser, PermissionsMixin):

    ROLE_CHOICES = (
            ('rider', 'Rider'),
            ('driver', 'Driver'),
            ('admin', 'Admin'),
        )
    
    email = models.EmailField(_('email address'), unique=True)
    phone = PhoneNumberField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    objects = CustomAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'first_name','last_name']

    def __str__(self):
        return self.email

class DriverProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=50)
    plate_number = models.CharField(max_length=20, unique=True)
    vehicle_color = models.CharField(max_length=30, blank=True)
    vehicle_year = models.PositiveIntegerField(blank=True, null=True)
    vehicle_type = models.CharField(max_length=30)
    vehicle_model = models.CharField(max_length=30)
    verified = models.BooleanField(default=False)
    documents = models.FileField(upload_to="driver_docs/")

    def __str__(self):
        return self.license_number
    
    