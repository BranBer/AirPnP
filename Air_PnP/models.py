from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.query import QuerySet
from datetime import datetime
from django.utils import timezone

from django.contrib.auth.models import AbstractBaseUser

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from Air_PnP.managers import MyUserManager


class Users(AbstractBaseUser):
    username = models.CharField(max_length = 20, null = False, blank = False, unique = True, primary_key = True)
    personalEmail = models.CharField(max_length = 50, unique = True)
    first_name = models.CharField(max_length = 20, null = False, blank = False)
    last_name = models.CharField(max_length = 20, null = False, blank = False)
    home_address = models.CharField(max_length = 150, null = False, blank = True, default = '')
    
    date_joined = models.DateTimeField(auto_now_add = True)
    last_login = models.DateTimeField(default = timezone.now)
    is_admin = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)
 
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('personalEmail', 'first_name', 'last_name', 'home_address')

    objects = MyUserManager()

    def __str__(self):
        return self.username + ", " + self.personalEmail

    def has_perm(self, perm, obj = None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True


class Addresses(models.Model):
    user = models.ForeignKey(Users, related_name='addresses', on_delete = models.CASCADE)
    address_line1 = models.CharField(max_length = 45, null = False, blank = False)
    address_line2 = models.CharField(max_length = 45, null = True, blank = True)
    city = models.CharField(max_length = 20, null = False, blank = False)
    state = models.CharField(max_length = 2, null = False, blank = False)
    zip = models.IntegerField(null = False, blank = False)
    longitude = models.DecimalField(max_digits=21, decimal_places=15)
    latitude = models.DecimalField(max_digits=18, decimal_places=15)

class Payment_Info(models.Model):
    email = models.CharField(max_length = 30, null = False, blank = False, primary_key = True, unique = True)
    user = models.OneToOneField(Users, on_delete = models.CASCADE)
    
class Invoices(models.Model):
    amount = models.DecimalField(max_digits = 6, decimal_places = 2)
    date = models.DateTimeField(null = False, blank = False, default= datetime.now)
    payer = models.ForeignKey(Payment_Info, related_name = 'payer', on_delete = models.DO_NOTHING)
    payee = models.ForeignKey(Payment_Info, related_name = 'payee', on_delete = models.DO_NOTHING)

class Bathrooms(models.Model):
    address_id = models.ForeignKey(Addresses, on_delete = models.CASCADE, related_name = "bathrooms")
    has_shower = models.BooleanField(null = True)
    has_bath = models.BooleanField(null = True)
    has_sink = models.BooleanField(null = True)
    has_fem_products = models.BooleanField(null = True)
    has_toilet_paper = models.BooleanField(null = True)
    num_of_toilets = models.IntegerField(default = 0)


class Ratings(models.Model):
    user = models.ForeignKey(Users, on_delete = models.CASCADE)
    bathroom_id = models.ForeignKey(Bathrooms, on_delete = models.CASCADE, related_name = "ratings")
    score = models.IntegerField(default = 0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    title = models.CharField(max_length = 30, blank = True)
    description = models.CharField(max_length = 200)

@receiver(post_save, sender = settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance = None, created = False, **kwargs):
    if created:
        Token.objects.create(user=instance)