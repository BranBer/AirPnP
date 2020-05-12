from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework import exceptions 
from Air_PnP.models import *

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
        fields = ['user', 'bathroom_id', 'score', 'title', 'description']

class TimesAvailable_Serializer(serializers.ModelSerializer):
    class Meta:
        model = TimesAvailable
        fields = ['week_day', 'open_time', 'close_time', 'users']

class DayAvailable_Serializer(serializers.ModelSerializer):
    timesAvailable = TimesAvailable_Serializer(many = False, read_only = True)
    class Meta:
        model = DayAvailable
        fields = ['bathroom_id', 'week_day', 'timesAvailable']

class PricingOption_Serializer(serializers.ModelSerializer):
    class Meta:
        model = PricingOption
        fields = ['bathroom_id', 'timePeriod', 'amount']

class BathroomPost_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Bathrooms
        fields = '__all__'

class Bathrooms_Serializer(serializers.ModelSerializer):
    ratings = Ratings_Serializer(many = True, read_only = True)
    #pricing = PricingOption_Serializer(many = True, read_only = True)
    #avgRatings = Bathroom_Score_Avg_Serializer(many = True, read_only = True)

    class Meta:
        model = Bathrooms
        depth = 1
        fields = ['id', 'address_id', 'has_shower', 'has_bath', 'has_sink', 'has_fem_products', 'num_of_toilets', 'has_toilet_paper', 'ratings', 'image1', 'image2', 'image3', 'image4']
    
class Scheduler_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Scheduler
        fields = ['user', 'bathroom', 'date']
        
class Addresses_Serializer(serializers.ModelSerializer):
    bathrooms = Bathrooms_Serializer(many = True, read_only = True)
    class Meta:
        model = Addresses
        fields = ['id', 'user', 'address_line1', 'address_line2', 'city', 'state', 'zip', 'longitude', 'latitude', 'bathrooms']

class Users_Serializer(serializers.ModelSerializer):
    addresses = Addresses_Serializer(many = True, read_only = True)
    class Meta:
        model = Users
        fields = ['username', 'personalEmail', 'user_image', 'first_name', 'last_name', 'home_address', 'addresses']

class Registration_Serializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style = {'input_type': 'password'}, write_only = True)
    
    class Meta:
        model = Users
        fields = ['username', 'personalEmail', 'first_name', 'user_image', 'last_name', 'home_address', 'home_city', 'home_state', 'home_zip', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = Users(
            username = self.validated_data['username'],                
            personalEmail = self.validated_data['personalEmail'],
            first_name = self.validated_data['first_name'],
            last_name = self.validated_data['last_name'],
            home_address = self.validated_data['home_address'],
            home_state = self.validated_data['home_state'],
            home_city = self.validated_data['home_city'],
            home_zip = int(self.validated_data['home_zip']),
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if (password != password2):
            raise serializers.ValidationError({'password': 'Passwords must match.'})

        user.set_password(password)
        user.save()
        return user