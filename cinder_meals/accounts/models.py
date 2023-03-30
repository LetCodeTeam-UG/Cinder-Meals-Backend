from django.db import models
# trunk-ignore(flake8/F401)
from django.contrib.auth.models import AbstractUser, BaseUserManager
from .managers import AccountManager

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, null= True)
    phone = models.CharField(max_length=20, null= True)
    dob = models.DateField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_customer = models.BooleanField(default = False)
    is_staff = models.BooleanField(default=False)
    is_courier = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = AccountManager()
    
    class Meta:
        db_table = 'users'

    # def get_name(self):
    #     return self.fullname or self.email

    def __str__(self):
        return self.email


class Phone(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='phones')
    number = models.CharField(max_length=20)
    otp = models.CharField(max_length=6)
    verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.number