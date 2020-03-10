from django.shortcuts import render
from Air_PnP.forms import *
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import Template, Context, loader
from Air_PnP.serializers import *
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
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
        serializer = Bathrooms_Serializer(data=data)
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