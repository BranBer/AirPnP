from django.forms import ModelForm
from django import forms
from Air_PnP.models import *

class User_Form(ModelForm):
    #password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Users
        fields = ['username', 'password', 'personalEmail', 'first_name', 'last_name', 'home_address']

class Addresses_Form(ModelForm):
    class Meta:
        model = Addresses
        fields = ['user', 'address_line1', 'address_line2', 'city', 'state', 'zip', 'longitude', 'latitude']

class Payment_Info_Form(ModelForm):
    class Meta:
        model = Payment_Info
        fields = ['email', 'user']


class Invoices_Form(ModelForm):
    class Meta:
        model = Invoices
        fields = ['amount', 'payer', 'payee']

class Bathrooms_Form(ModelForm):
    class Meta:
        model = Bathrooms
        fields = ['address_id', 'has_shower', 'has_bath', 'has_sink', 'has_fem_products', 'num_of_toilets']

class Ratings_Form(ModelForm):
    class Meta:
        model = Ratings
        fields = ['user', 'bathroom_id','score','title','description']
        

