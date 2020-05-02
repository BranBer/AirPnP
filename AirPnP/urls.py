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
from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', Home_View),
    path('admin', admin.site.urls),
    path('User/', Create_User, name = 'User'),
    path('User/API', Users_API, name = 'User_API'),
    path('User/register', registerUser),
    path('User/login/', custom_login),
    path('User/Addresses', Create_Addresses, name = 'Addresses'),
    path('User/Addresses/API', Addresses_API, name = 'Address_API'),
    path('User/Addresses/Create/', PostToAddressesAPI),
    path('User/Addresses/FromToken/', getAddressFromToken),
    path('User/PaymentInfo', Create_Payment_Info, name = 'Payment_Info'),
    path('User/PaymentInfo/API', Payment_Info_API, name = 'Payment_Info_API'),
    path('User/PaymentInfo/AddUserPaymentInfo/', PostToPaymentInfoAPI),
    path('User/SecureGetUserFromToken/', secureGetUserFromToken),
    path('Bathrooms/post/', bathroomPost),
    path('Bathrooms', Create_Bathrooms, name = 'Bathrooms'),
    path('Bathrooms/API', Bathrooms_API, name = 'Bathrooms_API'),
    path('Bathrooms/Create/', Bathrooms_Post_API),
    path('Bathrooms/Ratings', Create_Ratings, name = 'Ratings'),
    path('Bathrooms/Ratings/API', Ratings_API, name = 'Ratings_API'),
    path('Bathrooms/API/<int:id>/', getBathroomByID),
    path('Bathrooms/DaysAvailable/', DayAvailableAPI), #Shows all the days of the week for all bathrooms. Times available are nested in each day along with users that reserved the bathroom within those times available 
    path('Bathrooms/DaysAvailable/<int:bathroom_id>/', availabilityForBathrooms),
    path('Bathrooms/CreateTimeSlot/', createBathroomAvailability), #Creates an availability for a bathroom given that the user of the current token in the header owns the bathroom
    path('Bathrooms/ReserveBathroom/', reserveBathroom), #Reserves a bathroom for the user of the current authtoken header
    path('Bathrooms/CreatePricingOption/<int:bathroom_id>/<how_long>/<amount>/', createBathroomPricingOption), #Creates a pricing option for a bathroom given thatthe user of the current token in the header owns the bathroom
    path('Bathrooms/PricingOptions/API/', PricingOptionsAPI), #Returns all the pricing options for all bathrooms
    path('Bathrooms/PricingOptions/<int:bathroom_id>/', PricingOptionsForBathroom), #Returns all the pricing options available for a user when reserving a bathroom
    path('Bathrooms/Appointments/<int:bathroom_id>/', getAppointmentsForBathroom), #Returns all the schedules appointments for a bathroom
    path('Invoices', Create_Invoices, name = 'Invoices'),
    path('Invoices/API', Invoices_API, name = 'Invoices_API'),
    path('Invoices/API/<amount>/<str:payer>/<str:payee>/', PostToInvoicesAPI),
    path('User/Addresses/API/bycoords/<lat>/<lon>/', GetNearbyBathroomsAPI),
    path('User/Addresses/API/top5incity/<str:city>/<str:state>/', top5BathroomsInCity),
    path('User/Addresses/API/top5all/', top5Bathrooms),
    path('User/API/getuser/<str:usern>/', getUser),
    path('Schedule/API/', SchedulerAPI),
    path('TestUserAPI', testAuthView),
]
