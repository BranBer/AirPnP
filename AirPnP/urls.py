"""AirPnP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Air_PnP.views import *

urlpatterns = [
    path('', Home_View),
    path('User/', Create_User, name = 'User'),
    path('User/API', Users_API, name = 'User_API'),
    path('User/API/<str:username>/<str:password>/<str:personalEmail>/<str:first_name>/<str:last_name>/', PostToUsersAPI),
    path('User/Addresses', Create_Addresses, name = 'Addresses'),
    path('User/Addresses/API', Addresses_API, name = 'Address_API'),
    path('User/Addresses/API/<str:user>/<str:address_line1>/<str:address_line2>/<str:city>/<str:state>/<int:zip>/<longitude>/<latitude>/', PostToAddressesAPI),
    path('User/PaymentInfo', Create_Payment_Info, name = 'Payment_Info'),
    path('User/PaymentInfo/API', Payment_Info_API, name = 'Payment_Info_API'),
    path('User/PaymentInfo/API/<str:user>/<str:email>/', PostToPaymentInfoAPI),
    path('Bathrooms', Create_Bathrooms, name = 'Bathrooms'),
    path('Bathrooms/API', Bathrooms_API, name = 'Bathrooms_API'),
    path('Bathrooms/API/<int:address_id>/<int:has_shower>/<int:has_bath>/<int:has_sink>/<int:has_fem_products>/<int:has_toilet_paper>/<int:num_of_toilets>/', PostToBathroomAPI),
    path('Bathrooms/Ratings', Create_Ratings, name = 'Ratings'),
    path('Bathrooms/Ratings/API', Ratings_API, name = 'Ratings_API'),
     path('Bathrooms/Ratings/API/<str:user>/<int:bathroom_id>/<int:score>/<str:title>/<str:description>/', PostToRatingsAPI),
    path('Invoices', Create_Invoices, name = 'Invoices'),
    path('Invoices/API', Invoices_API, name = 'Invoices_API'),
    path('Invoices/API/<amount>/<str:payer>/<str:payee>/', PostToInvoicesAPI),
    path('User/Addresses/API/bycoords/<lat>/<lon>/', GetNearbyBathroomsAPI),
    path('User/Addresses/API/top5incity/<str:city>/<str:state>/', top5BathroomsInCity),
    path('User/Addresses/API/top5all/', top5Bathrooms),
    path('User/API/getuser/<str:usern>/', getUser),
    path('User/API/login/<str:usern>/<str:passw>/', usernamePassword)
]
