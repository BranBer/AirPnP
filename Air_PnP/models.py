from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.query import QuerySet
from datetime import datetime

class Users(models.Model):
    username = models.CharField(max_length = 20, null = False, blank = False, unique = True, primary_key = True)
    personalEmail = models.CharField(max_length = 30, unique = True)
    password = models.CharField(max_length = 20, null = False, blank = False)
    first_name = models.CharField(max_length = 20, null = False, blank = False)
    last_name = models.CharField(max_length = 20, null = False, blank = False)
    home_address = models.CharField(max_length = 150, null = False, blank = True, default = '')
    
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

