from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager

# Create your models here.

class AddressChoices(models.TextChoices):
    HOME = 'HOME', 'Home'
    OFFICE = 'OFFICE', 'Office'
    OTHER = 'OTHER', 'Other'


class CustomerManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomerProfile(AbstractUser):

    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomerManager() 

    def __str__(self):
        return self.email
    
class Address(models.Model):

    customer = models.ForeignKey('CustomerProfile', on_delete=models.CASCADE,related_name='addresses' )
    address_type = models.CharField( max_length=50,choices=AddressChoices.choices , default=AddressChoices.HOME)
    address = models.CharField(max_length=225)
    phone_number = models.CharField(max_length=15)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    state = models.CharField(max_length=50)
    county = models.CharField(max_length=50, default='India')

    def __str__(self):
        return f"{self.address_type} - {self.customer.email}"