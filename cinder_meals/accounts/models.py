from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from .managers import AccountManager

class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_courier = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    objects = AccountManager()
    
    class Meta:
        db_table = 'users'

    def get_name(self):
        return self.fullname or self.username

    def __str__(self):
        return self.email


class Phone(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='phones')
    number = models.CharField(max_length=20)
    otp = models.CharField(max_length=6)
    verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.number