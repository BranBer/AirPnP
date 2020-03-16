from rest_framework import serializers
from Air_PnP.models import *

class Users_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username', 'personalEmail', 'password', 'first_name', 'last_name']

class Payment_Info_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Payment_Info
        fields = ['email', 'user']

class Invoices_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Invoices
        fields = ['amount', 'date', 'payer', 'payee']


class Ratings_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Ratings
        fields = ['user', 'bathroom_id','score','title','description']

class Bathrooms_Serializer(serializers.ModelSerializer):
    ratings = Ratings_Serializer(many = True, read_only = True)  
    #addresses = Addresses_Serializer(many = True, read_only = True)     
    #addresses = Addresses_Serializer(read_only = True)
    class Meta:
        model = Bathrooms
        fields = ['id', 'address_id', 'has_shower', 'has_bath', 'has_sink', 'has_fem_products', 'num_of_toilets', 'ratings']

class Addresses_Serializer(serializers.ModelSerializer):
    bathrooms = Bathrooms_Serializer(many = True, read_only = True)
    class Meta:
        model = Addresses
        fields = ['user', 'id', 'address_line1', 'address_line2', 'city', 'state', 'zip', 'longitude', 'latitude', 'bathrooms']