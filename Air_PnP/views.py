from django.shortcuts import render
from Air_PnP.forms import *
from Air_PnP.models import *
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import Template, Context, loader
from Air_PnP.serializers import *
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.db.models.query import QuerySet
from django.db.models import Avg
#from django.db.models import When

import datetime
# Create your views here.

def Home_View(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

def Create_User(request):
    form = User_Form(request.POST)

    if (form.is_valid()):
        post = form.save()

    return render (request, 'user_form.html' , {'form': form, 'form_title': 'Enter User Data'})

def Create_Addresses(request):
    form = Addresses_Form(request.POST)

    if (form.is_valid()):
        post = form.save()

    return render (request, 'address_form.html' , {'form': form, 'form_title': 'Enter User Addresses Info'})

def Create_Payment_Info(request):
    form = Payment_Info_Form(request.POST)

    if (form.is_valid()):
        post = form.save()

    return render (request, 'payment_info_form.html' , {'form': form, 'form_title': 'Enter User Payment Info'})

def Create_Invoices(request):
    form = Invoices_Form(request.POST)

    if (form.is_valid()):
        post = form.save()

    return render (request, 'invoice_form.html' , {'form': form, 'form_title': 'Enter Invoices'})

def Create_Bathrooms(request):
    form = Bathrooms_Form(request.POST)
    if (form.is_valid()):
        post = form.save()

    link = 'Ratings'
    link_name = 'Bathroom Ratings'

    return render (request, 'bathroom_form.html' , {'form': form, 'form_title': 'Enter Bathroom Data'})

def Create_Ratings(request):
    form = Ratings_Form(request.POST)

    if (form.is_valid()):
        post = form.save()

    return render (request, 'rating_form.html' , {'form': form, 'form_title': 'Enter User Rating'})


#Rest API Views
def Users_API(request):
    if request.method == 'GET':
        user = Users.objects.all()
        serializer = Users_Serializer(user, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = Users_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def Addresses_API(request):
    if request.method == 'GET':
        addresses = Addresses.objects.all()
        serializer = Addresses_Serializer(addresses, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = Addresses_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def Payment_Info_API(request):
    if request.method == 'GET':
        pay = Payment_Info.objects.all()
        serializer = Payment_Info_Serializer(pay, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = Payment_Info_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def Invoices_API(request):
    if request.method == 'GET':
        invoice = Invoices.objects.all()
        serializer = Invoices_Serializer(invoice, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = Invoices_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def Bathrooms_API(request):
    if request.method == 'GET':
        bathroom = Bathrooms.objects.all()
        serializer = Bathrooms_Serializer(bathroom, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        #serializer = Bathrooms_Serializer(data=data)
        serializer = Bathrooms_Serializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def Ratings_API(request):
    if request.method == 'GET':
        rating = Ratings.objects.all()
        serializer = Ratings_Serializer(rating, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = Ratings_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def PostToUsersAPI(request, username, password, personalEmail, first_name, last_name):
    user = Users(username = username, password = password, personalEmail = personalEmail, first_name = first_name, last_name = last_name)
    user.save()

    if request.method == 'GET':
        user = Users.objects.all()
        serializer = Users_Serializer(user, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = Users_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def PostToAddressesAPI(request, user, address_line1, address_line2, city, state, zip, longitude, latitude):
    myUser = Users.objects.get(pk = user)
    
    address = Addresses(address_line1 = address_line1, address_line2 = address_line2, city = city, state = state, zip = zip, longitude = longitude, latitude = latitude)
    address.save()

    address.user.add(myUser)

    if request.method == 'GET':
        addresses = Addresses.objects.all()
        serializer = Addresses_Serializer(addresses, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = Addresses_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def PostToPaymentInfoAPI(request, user, email):
    myUser = Users.objects.get(pk = user)

    payment_info = Payment_Info(email = email)
    payment_info.user = myUser
    payment_info.save()

    if request.method == 'GET':
        pay = Payment_Info.objects.all()
        serializer = Payment_Info_Serializer(pay, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = Payment_Info_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def PostToBathroomAPI(request, address_id, has_shower, has_bath, has_sink, has_fem_products, has_toilet_paper, num_of_toilets):
    address = Addresses.objects.get(pk = address_id)
    bathroom = Bathrooms(address_id = address, has_shower = bool(has_shower), has_bath = bool(has_bath), has_sink = bool(has_sink), has_fem_products = bool(has_fem_products), has_toilet_paper = bool(has_toilet_paper), num_of_toilets = num_of_toilets)
    bathroom.save()

    if request.method == 'GET':
        bathroom = Bathrooms.objects.all()
        serializer = Bathrooms_Serializer(bathroom, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = Bathrooms_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def PostToRatingsAPI(request, user, bathroom_id, score, title, description):
    myUser = Users.objects.get(pk = user)
    myBathroom = Bathrooms.objects.get(pk = bathroom_id)
    rating = Ratings(user = myUser, bathroom_id = myBathroom, score = score, title = title, description = description)
    rating.save()

    if request.method == 'GET':
        rating = Ratings.objects.all()
        serializer = Ratings_Serializer(rating, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = Ratings_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def PostToInvoicesAPI(request, amount, year, month, day, hour, minute, payer, payee):
    date = datetime.datetime(year = year, month = month, day = day, hour = hour, minute = minute)
    
    payerUser = Users.objects.get(pk = payer)
    payeeUser = Users.objects.get(pk = payee)

    payerInfo = Payment_Info.objects.get(user = payerUser)
    payeeInfo = Payment_Info.objects.get(user = payeeUser)

    invoice = Invoices(amount = amount, date = date, payer = payerInfo, payee = payeeInfo)
    invoice.save()

    if request.method == 'GET':
        invoice = Invoices.objects.all()
        serializer = Invoices_Serializ
        r(invoice, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = Invoices_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def GetNearbyBathroomsAPI(request, lat, lon):
    lat = float(lat)
    lon = float(lon)

    minLat = lat - 1.00000
    maxLat = lat + 1.00000

    minLon = lon - 1.00000
    maxLon = lon + 1.00000
 
    #addresses = Addresses.objects.filter(latitude__range = (minLat, maxLat), longitude__range = (minLon, maxLon))

    if request.method == 'GET':
        addresses = Addresses.objects.filter(latitude__range = (minLat, maxLat), longitude__range = (minLon, maxLon))
        serializer = Addresses_Serializer(addresses, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = Addresses_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def top5BathroomsInCity(request, city, state):
    a = Addresses.objects.filter(city__iexact = city, state__iexact = state).values('id')
    b = Bathrooms.objects.filter(address_id__in = a).values('id')
    r = Ratings.objects.filter(bathroom_id__in = b).values('bathroom_id').annotate(avsc = Avg('score')).order_by('-avsc')[:5]    
    r_id = r.values('bathroom_id')  
    
    top5b = Bathrooms.objects.filter(id__in = r_id) 

    if request.method == 'GET':
        #top5b = Bathrooms.objects.all()
        serializer = Bathrooms_Serializer(top5b, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = Bathrooms_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    




