from django.shortcuts import render
from Air_PnP.forms import *
from Air_PnP.models import *
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import Template, Context, loader
from Air_PnP.serializers import *

from django.contrib.auth import authenticate
from rest_framework.authtoken.views import ObtainAuthToken

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes, throttle_classes

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


from django.db.models.query import QuerySet
from django.db.models import Avg

#from django.db.models import When

from datetime import datetime
from datetime import timedelta
# Create your views here.

def Home_View(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

def testAuthView(request, format=None):
    content = {
        'user': unicode(request.user),
        'auth': unicode(request.auth),
    }

    return Response(content)

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
        #sun = DayAvailable(post.id, 'Sunday')
        #sun.save()
        #mon = DayAvailable(post.id, 'Monday')
        #mon.save()
        #tue = DayAvailable(post.id, 'Tuesday')
        #tue.save()
        #wed = DayAvailable(post.id, 'Wednesday')
        #wed.save()
        #thur = DayAvailable(post.id, 'Thursday')
        #thur.save()
        #fri = DayAvailable(post.id, 'Friday')
        #fri.save()
        #sat = DayAvailable(post.id, 'Saturday')
        #sat.save()         

    #link = 'Ratings'
    #link_name = 'Bathroom Ratings'

    return render (request, 'bathroom_form.html' , {'form': form, 'form_title': 'Enter Bathroom Data'})

def Create_Ratings(request):
    form = Ratings_Form(request.POST)

    if (form.is_valid()):
        post = form.save()

    return render (request, 'rating_form.html' , {'form': form, 'form_title': 'Enter User Rating'})

#Rest API Views
#@api_view(['GET', 'POST'])
#@permission_classes([IsAuthenticated])

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@throttle_classes([UserRateThrottle])
def Users_API(request):
    u = Users.objects.all()
    ser = Users_Serializer(u, many = True)

    return JsonResponse(ser.data, safe = False)

@api_view(['POST',])
@throttle_classes([AnonRateThrottle])
def registerUser(request):
    if request.method == 'POST':
        serializer = Registration_Serializer(data = request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "Successfully registered a new user"
            #data['username'] = user.username
            #data['personalEmail'] = user.personalEmail
        else:
            data = serializer.errors
            
        return JsonResponse(data, safe = False)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@throttle_classes([UserRateThrottle])
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

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@throttle_classes([UserRateThrottle])
def Payment_Info_API(request):
    if request.method == 'GET' and Token.objects.get(key = request.headers.get('Authorization')[6:]).user.is_superuser:
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

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@throttle_classes([UserRateThrottle])
def Invoices_API(request):
    user = Token.objects.get(key = request.headers.get('Authorization')[6:]).user
    if request.method == 'GET' and user.is_superuser:
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


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@throttle_classes([UserRateThrottle])
def Bathrooms_API(request):
    bathroom = Bathrooms.objects.all()
    serializer = Bathrooms_Serializer(bathroom, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@throttle_classes([UserRateThrottle])
def Bathrooms_Post_API(request):
    try:
        bathroom = BathroomPost_Serializer(data = request.data)
        requestAuthToken = request.headers.get('Authorization')
        user = Token.objects.get(key = requestAuthToken[6:]).user

        address = Addresses.objects.get(id = int(request.data['address_id']))
    
        if bathroom.is_valid():
            if address.user.username == user.username:
                bathroom.save()
                return JsonResponse(bathroom.data, safe = False)
            else:
                return JsonResponse("You must own the address to create a bathroom in it!", safe = False)
        else:
            return JsonResponse("Invalid data", safe = False)
    except Token.DoesNotExist:
        return JsonResponse("User does not exist", safe = False)
    except Addresses.DoesNotExist:
        return JsonResponse("Address does not exist")   
    
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@throttle_classes([UserRateThrottle])
def Ratings_API(request):
    rating = Ratings.objects.all()
    serializer = Ratings_Serializer(rating, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@throttle_classes([UserRateThrottle])
def MakeARating(request):
    try:
        user = Token.objects.get(key = request.headers.get('Authorization')[6:]).user
        bathroom_id = int(request.data['bathroom_id'])
        b = Bathrooms.objects.get(id = bathroom_id)

        if(b.address_id.user.username != user.username):
            score = int(request.data['score'])
            title = request.data['title']
            description = request.data['description']

            r = Ratings.objects.create(user = user, bathroom_id = b, score = score, title = title, description = description)
            serializer = Ratings_Serializer(r, many = False)

            return JsonResponse(serializer.data, safe = False)
        else:
            return JsonResponse('Bathroom Owners cannot make reviews for their own bathrooms!', safe = False)
    except Token.DoesNotExist:
        return JsonResponse('Invalid Token', safe = False)
    except Bathrooms.DoesNotExist:
        return JsonResponse('Bathroom Does Not Exist', safe = False)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@throttle_classes([UserRateThrottle])
def DayAvailableAPI(request):
    if request.method == 'GET':
        days = DayAvailable.objects.all()
        serializer = DayAvailable_Serializer(days, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = DayAvailable_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@throttle_classes([UserRateThrottle])
def PricingOptionsAPI(request):
    if request.method == 'GET':
        prices = PricingOption.objects.all()
        serializer = PricingOption_Serializer(prices, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PricingOption_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@throttle_classes([UserRateThrottle])
def PricingOptionsForBathroom(request, bathroom_id):
    if request.method == 'GET':
        prices = PricingOption.objects.filter(bathroom_id__exact = bathroom_id)
        serializer = PricingOption_Serializer(prices, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PricingOption_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@throttle_classes([UserRateThrottle])
def PostToAddressesAPI(request): #, user, address_line1, address_line2, city, state, zip, longitude, latitude):
    #myUser = Users.objects.get(pk = user)
    #address = Addresses(address_line1 = address_line1, address_line2 = address_line2, city = city, state = state, zip = zip, longitude = longitude, latitude = latitude)
    #address.save()
    #address.user.add(myUser)

    try:   
        requestAuthToken = request.headers.get('Authorization')
        user = Token.objects.get(key = requestAuthToken[6:]).user

        if request.method == 'POST':
            data = request.data
            #data.GET['username'] = user.username
        
            #user = user.username 
            address_line1 = data['address_line1']
            address_line2 = data['address_line2']
            city = data['city']
            state = data['state']
            zip = data['zip']
            longitude = float(data['longitude'])
            latitude = float(data['latitude'])

            a = Addresses.objects.create(
                user = user, 
                address_line1 = address_line1, 
                address_line2 = address_line2,
                city = city,
                state = state,
                zip = zip,
                longitude = longitude,
                latitude = latitude)

            serializer = Addresses_Serializer(a, many = False)
            return JsonResponse(serializer.data, safe=False)
    except Token.DoesNotExist:
         return JsonResponse("Token does not exist.", safe=False)
    except Address.DoesNotExist:
         return JsonResponse("Something went wrong.", safe=False)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@throttle_classes([UserRateThrottle])
def PostToPaymentInfoAPI(request):
    try:
        data = {}
        requestAuthToken = request.headers.get('Authorization')
        user = Token.objects.get(key = requestAuthToken[6:]).user

        email = request.data['email']

        p = Payment_Info.objects.create(email = email, user = user)
    
        data['user'] = p.user.username
        data['email'] = p.email 
    
    #serializer = Payment_Info_Serializer(p, many = False)
        
        return JsonResponse(data, safe = False)
    except:
        return JsonResponse("User doesn't exist / Can't use someone else's payment info", safe = False)

@api_view(['GET',])
@permission_classes((IsAuthenticated,))
@throttle_classes([UserRateThrottle])
def PostToBathroomAPI(request, address_id, has_shower, has_bath, has_sink, has_fem_products, has_toilet_paper, num_of_toilets):
    if request.method == 'GET':
        #Get corresponding address object
        address = Addresses.objects.get(pk = address_id)
        bathroom = Bathrooms(address_id = address, has_shower = bool(has_shower), has_bath = bool(has_bath), has_sink = bool(has_sink), has_fem_products = bool(has_fem_products), has_toilet_paper = bool(has_toilet_paper), num_of_toilets = num_of_toilets)
        bathroom.save()

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

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@throttle_classes([UserRateThrottle])
def PostToInvoicesAPI(request, amount, payer, payee):
    payerUser = Users.objects.get(pk = payer)
    payeeUser = Users.objects.get(pk = payee)

    payerInfo = Payment_Info.objects.get(user = payerUser)
    payeeInfo = Payment_Info.objects.get(user = payeeUser)

    invoice = Invoices(amount = amount, payer = payerInfo, payee = payeeInfo)
    invoice.save()

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

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@throttle_classes([UserRateThrottle])
def GetNearbyBathroomsAPI(request, lat, lon):
    lat = float(lat)
    lon = float(lon)

    minLat = lat - 1.00000
    maxLat = lat + 1.00000

    minLon = lon - 1.00000
    maxLon = lon + 1.00000
 
    #addresses = Addresses.objects.filter(latitude__range = (minLat, maxLat), longitude__range = (minLon, maxLon))
    addresses = Addresses.objects.filter(latitude__range = (minLat, maxLat), longitude__range = (minLon, maxLon)).values('id')
    bathroom = Bathrooms.objects.filter(address_id__in = addresses)

    if request.method == 'GET':
        #bathroom = Bathrooms.objects.all()
        serializer = Bathrooms_Serializer(bathroom, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = Bathrooms_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@throttle_classes([UserRateThrottle])
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

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@throttle_classes([UserRateThrottle])
def top5Bathrooms(request):
    b = Bathrooms.objects.all().values('id')
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

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@throttle_classes([UserRateThrottle])  
def getUser(request, usern):
    user = Users.objects.filter(username__iexact = usern)

    if request.method == 'GET':
        serializer = Users_Serializer(user, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = Users_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@throttle_classes([UserRateThrottle])
def getBathroomByID(request, id):
    bathroom = Bathrooms.objects.filter(id__exact = id)
    
    if request.method == 'GET':
        #bathroom = Bathrooms.objects.all()
        serializer = Bathrooms_Serializer(bathroom, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = Bathrooms_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@throttle_classes([UserRateThrottle])
def getUserToken(request, usern, passw):
    user = None
    data = {}

    try:
        user = Users.objects.get(username = usern)
        
        if(user.is_superuser):
            user = authenticate(username = usern, password = passw)
        else:
            user = Users.objects.get(username = usern, password = passw)

    except Users.DoesNotExist:
        return HttpResponse("No User Found")


    if user is not None:
        if request.method == 'GET':   
            token = Token.objects.get(user=user).key
            data['username'] = user.username
            data['token'] = token

            return JsonResponse(data)
    else:
        return HttpResponse("No User Found")
    

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@throttle_classes([UserRateThrottle])
def bathroomPost(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = Bathrooms_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@api_view(['GET',])
@permission_classes((IsAuthenticated,))
@throttle_classes([UserRateThrottle])
def getUserFromToken(request, token):
    users = Users.objects.filter()
    u = None
    data = {}

    for user in users:
        userToken = Token.objects.get(user=user).key
        if(token == userToken):
            u = user
            if request.method == 'GET':
                data['username'] = u.username
                data['personalEmail'] = u.personalEmail
                data['first_name'] = u.first_name
                data['last_name'] = u.last_name
                data['home_address'] = u.home_address
                data['home_state'] = u.home_state
                data['home_city'] = u.home_city
                data['home_zip'] = u.home_zip
                data['token'] = userToken

                return JsonResponse(data, safe=False)
                #serializer = Users_Serializer(u, many=True)
                #return JsonResponse(serializer.data, safe=False)
            
    return JsonResponse('Invalid Token', safe=False)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@throttle_classes([UserRateThrottle])
def secureGetUserFromToken(request):
    users = Users.objects.filter()
    u = None
    data = {}

    requestAuthToken = request.headers.get('Authorization')

    for user in users:
        userToken = Token.objects.get(user=user).key
        if(requestAuthToken[6:] == userToken):
            u = user
            if request.method == 'GET' and u != None:                            
                #return JsonResponse('got here', safe=False)
                serializer = Users_Serializer(u, many=False)
                return JsonResponse(serializer.data, safe=False)
    
    return JsonResponse('Invalid Token!', safe=False)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@throttle_classes([UserRateThrottle])
def createBathroomAvailability(request):#, bathroom_id, week_day, open_time, close_time):
    data = {}
    bathroom_id = int(request.data['bathroom_id'])
    week_day = request.data['week_day']
    open_time = request.data['open_time']
    close_time = request.data['close_time']

    open_time = datetime.strptime(open_time, '%H:%M:%S').time()
    close_time = datetime.strptime(close_time, '%H:%M:%S').time()

    try:
        requestAuthToken = request.headers.get('Authorization')
        user = Token.objects.get(key = requestAuthToken[6:]).user

        bathroom = Bathrooms.objects.get(id = bathroom_id)

        if(bathroom.address_id.user.username == user.username):
            day = DayAvailable.objects.get(bathroom_id = bathroom, week_day = week_day)
            timeSlot = TimesAvailable.objects.create(week_day = day, open_time = open_time, close_time = close_time)

            data['bathroom_id'] = bathroom_id
            data['week_day'] = week_day
            data['open_time'] = str(open_time)
            data['close_time'] = str(close_time)

            return JsonResponse(data, safe = False)
        else:
            return JsonResponse("You must own the bathroom to create an availability. How did you get here?", safe = False)
    except (Bathrooms.DoesNotExist, DayAvailable.DoesNotExist) as e:
        return JsonResponse('Bathroom does not exist / Invalid Day')

    return JsonResponse('Bathroom does not exist', safe = False)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@throttle_classes([UserRateThrottle])
def reserveBathroom(request): #, bathroom_id, week_day, open_time, date, how_long):
    data = {}

    bathroom_id = request.data['bathroom_id']
    bathroom_id = int(bathroom_id)
    week_day = request.data['week_day']
    open_time = request.data['open_time']
    date = request.data['date']
    how_long = request.data['how_long']

    #return JsonResponse(request.data, safe = False)

    daysOfWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
    how_long = datetime.strptime(how_long, '%H:%M:%S')
    open_time = datetime.strptime(open_time, '%H:%M:%S')
    
    bathroom = Bathrooms.objects.filter(id = bathroom_id)
    user = None

    if(bathroom.count() > 0):                
        day = DayAvailable.objects.filter(bathroom_id = bathroom[0], week_day = week_day)
        
        #Checks to see if the auth token is valid. If not then it prematurely returns a JsonResponse detailing the error.
        try:
            requestAuthToken = request.headers.get('Authorization')
            user = Token.objects.get(key = requestAuthToken[6:]).user
            #user = Users.objects.get(username = username)
        except Token.DoesNotExist:
            return JsonResponse('Invalid Token', safe = False)
        except User.DoesNotExist:
            return JsonResponse('User does not exist', safe = False)
            
        
        #pricingOptions = PricingOption.objects.filter(bathroom_id = bathroom[0], timePeriod = how_long)
        #return JsonResponse('day: ' + str(day.count()) + ' price: ' + str(pricingOptions.count()), safe = False)
        #Checks to see if the day is available for the select bathroom and if their are pricing options listed for that bathroom.
        #If not then it prematurely returns a JsonResponse detailing the error.
        if(day.count() != 0 and daysOfWeek[date.weekday()] == week_day):# and pricingOptions.count() != 0):            
            #Get a timeslot if there is one available.                        
            reservedTime = TimesAvailable.objects.filter(week_day = day[0], open_time = open_time)
            #checks if the requested time of day is within the available bathroom hours.
            if(reservedTime.count() > 0 and date.time() < reservedTime[0].close_time and date.time() >= reservedTime[0].open_time):
                #return JsonResponse('Here', safe = False)
                #Checks to see if time slot does not overlap with others. If it does not overlap it creates a schedules time for a user at the requested bathroom.
                min = (how_long.hour * 60) + how_long.minute
                timeSpacing = date + timedelta(minutes = min)
                schedule = Scheduler.objects.filter(date__range = (date, timeSpacing))
                
                #Get the payment info for the bathroom owner and the customer and creates an invoice
                #try:
                #    #Get bathroom owner
                #    bathroomOwner = bathroom[0].address_id.user
                #    owner = Payment_Info.objects.get(user = bathroomOwner)
                #    customer = Payment_Info.objects.get(user = user)
                #    invoice = Invoices.objects.create(payer = customer, payee = owner, amount = pricingOptions[0].amount, date = datetime.now())
                #except (Payment_Info.DoesNotExist, Invoices.DoesNotExist) as e:
                #    return JsonResponse('Users do not have any payment information', safe = False)
                
                #Checks to see if the alloted time requested goes past the bathroom's hours.
                #If it does then it prematurely returns a JsonResponse detailing the error.
                if(timeSpacing.time() > reservedTime[0].close_time):
                    return JsonResponse('Unable to request for this time slot: Alloted time requested goes past the bathroom\'s closing time', safe = False)

                if(schedule.count() == 0):
                    data['username'] = user.username
                    data['bathroom_id'] = bathroom_id
                    data['week_day'] = week_day                    
                    data['date'] = str(date.date())
                    data['time'] = str(date.time())
                    data['minutes_alloted'] = min

                    reservedTime[0].users.add(user)
                    Scheduler.objects.create(user = user, bathroom = bathroom[0], date = date, duration = how_long)
                    
                    return JsonResponse(data, safe = False)

                return JsonResponse('Time slot is taken', safe = False)
            else:
                return JsonResponse('Time is unavailable', safe = False)

    return JsonResponse('Bathroom does not exist or pricing option does not exist', safe = False)

@api_view(['GET'])
#@permission_classes((IsAuthenticated,))
@throttle_classes([AnonRateThrottle])
def availabilityForBathrooms(request, bathroom_id):
    try:
        b = Bathrooms.objects.get(id = bathroom_id)

        days = DayAvailable.objects.filter(bathroom_id = b)
        serializer = DayAvailable_Serializer(days, many=True)
        return JsonResponse(serializer.data, safe=False)
    except Bathrooms.DoesNotExist:
        return JsonResponse('bathroom does not exist', safe=False)

@api_view(['GET'])
#@permission_classes((IsAuthenticated,))
@throttle_classes([UserRateThrottle])
def SchedulerAPI(request):
    if request.method == 'GET':
        schedule = Scheduler.objects.all()
        serializer = Scheduler_Serializer(schedule, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = Scheduler_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@api_view(['GET'])
#@permission_classes((IsAuthenticated,))
@throttle_classes([UserRateThrottle])
def getAppointmentsForBathroom(request, bathroom_id):
    try:
        bathroom = Bathrooms.objects.get(id = bathroom_id)

        if request.method == 'GET':
            schedule = Scheduler.objects.filter(bathroom = bathroom)
            serializer = Scheduler_Serializer(schedule, many=True)
            return JsonResponse(serializer.data, safe=False)

    except Bathrooms.DoesNotExist:
        return JsonResponse("Bathroom or Schedule does not exist", status=400)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@throttle_classes([UserRateThrottle])
def createBathroomPricingOption(request, bathroom_id, how_long, amount):
    #Makes sure that the bathroom is owned by the user with the current auth token in the request header so that
    #other users can't create pricing options for bathrooms they don't own
    how_long = datetime.strptime(how_long, "%H:%M:%S")
    amount = float(amount)

    requestAuthToken = request.headers.get('Authorization')
    user = Token.objects.get(key = requestAuthToken[6:]).user
    addresses = Addresses.objects.filter(user = user).values('id')
    b = Bathrooms.objects.filter(id = bathroom_id, address_id__in = addresses)
    data = {}

    if(b[0] != None):
        p = PricingOption.objects.create(bathroom_id = b[0], timePeriod = how_long, amount = amount)
        data['bathroom_id'] = bathroom_id
        data['how_long'] = how_long
        data['amount'] = amount

        return JsonResponse(data, safe = False)

    return JsonResponse('bathroom does not exist', safe = False)

@api_view(['POST'])
#@permission_classes((IsAuthenticated,))
@throttle_classes([AnonRateThrottle])
def custom_login(request):
    user = None
    username = None
    password = None
    data = {}

    try:
        username = request.data['username']
        password = request.data['password']
    except:
        return JsonResponse("Username and Password required!", safe = False)

    try:
        user = Users.objects.get(username = username)
        
        if(user.is_superuser):
            user = authenticate(username = username, password = password)
        else:
            user = Users.objects.get(username = username, password = password)

        token = Token.objects.get(user=user).key
        data['username'] = user.username
        data['token'] = token

        return JsonResponse(data, safe = False)

    except Users.DoesNotExist:
        try:
            user = authenticate(username = username, password = password)
            token = Token.objects.get(user=user).key
            data['username'] = user.username
            data['token'] = token
            
            return JsonResponse(data, safe = False)
        except:
            return JsonResponse("No user found", safe = False)

@api_view(['GET'])
@permission_classes((IsAuthenticated,)) 
@throttle_classes([UserRateThrottle])
def getAddressFromToken(request):
    try:
        requestAuthToken = request.headers.get('Authorization')
        user = Token.objects.get(key = requestAuthToken[6:]).user

        addresses = Addresses.objects.filter(user = user)
        serializer = Addresses_Serializer(addresses, many = True)

        return JsonResponse(serializer.data, safe = False)
        
    except Users.DoesNotExist:
        return JsonResponse("No user found", safe = False)
    except Token.DoesNotExist:
        return JsonResponse("Invalid Token", safe = False)
    
    return JsonResponse("No Addresses for User", safe = False)

#Model Updates
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@throttle_classes([UserRateThrottle])
def UpdateAddress(request):
    data = {}
    address_id = int(request.data['id'])

    try:
        requestAuthToken = request.headers.get('Authorization')
        user = Token.objects.get(key = requestAuthToken[6:]).user
    
        for key in request.data:
            if(key != 'id'):
               data[key] = request.data[key]

        updateThis = Addresses.objects.filter(id = address_id)

        if(updateThis[0].user.username == user.username):
            updateThis.update(**data)
            a = Addresses.objects.get(id = address_id)
            serializer = Addresses_Serializer(a, many = False)

            return JsonResponse(serializer.data, safe = False)

    except Token.DoesNotExist:
        return JsonResponse("Invalid Token", safe = False)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@throttle_classes([UserRateThrottle])
def UpdateUser(request):
    data = {}

    try:
        requestAuthToken = request.headers.get('Authorization')
        tokenUser = Token.objects.get(key = requestAuthToken[6:]).user
    
        for key in request.data:
            if(key == 'password'):
               return JsonResponse("Cannot change password here!", safe = False)
            if (key == 'username'):
                return JsonResponse("Cannot change username here!", safe = False)

            if (key == 'first_name'):
                tokenUser.first_name = request.data[key]
            if (key == 'last_name'):
                tokenUser.last_name = request.data[key]
            if (key == 'personalEmail'):
                tokenUser.personalEmail = request.data[key]
            if (key == 'home_address'):
                tokenUser.home_address = request.data[key]
            if (key == 'user_image'):
                tokenUser.user_image = request.FILES['user_image']
                    
        tokenUser.save()
        serializer = Users_Serializer(tokenUser, many = False)

        return JsonResponse(serializer.data, safe = False)
    except Token.DoesNotExist:
        return JsonResponse("Invalid Token", safe = False)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@throttle_classes([UserRateThrottle])
def UpdateBathroom(request):
    data = {}
    bathroom_id = int(request.data['id'])

    try:
        requestAuthToken = request.headers.get('Authorization')
        user = Token.objects.get(key = requestAuthToken[6:]).user
        b = Bathrooms.objects.get(id = bathroom_id)
    
        for key in request.data:
            if(key != 'id' and key != 'image1' and key != 'image2' and key != 'image3' and key != 'image4'):
               data[key] = request.data[key]

            if(key == 'image1'):
                b.image1 = request.FILES.get('image1')
            if(key == 'image2'):
                b.image2 = request.FILES.get('image2')
            if(key == 'image3'):
                b.image3 = request.FILES.get('image3')
            if(key == 'image4'):
                b.image4 = request.FILES.get('image4')
        
        b.save()

        updateThis = Bathrooms.objects.filter(id = bathroom_id)

        if(updateThis[0].address_id.user.username == user.username):
            updateThis.update(**data)
   
            serializer = Bathrooms_Serializer(b, many = False)

            return JsonResponse(serializer.data, safe = False)

    except Token.DoesNotExist:
        return JsonResponse("Invalid Token", safe = False)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@throttle_classes([UserRateThrottle])
def UpdateTimeSlot(request):
    data = {}
    bathroom_id = int(request.data['bathroom_id'])
    week_day = request.data['week_day']
    old_open_time = datetime.strptime(request.data['old_open_time'], '%H:%M:%S')

    try:
        requestAuthToken = request.headers.get('Authorization')
        user = Token.objects.get(key = requestAuthToken[6:]).user
    
        for key in request.data:
            if(key != 'bathroom_id' and key != 'old_open_time' and key != 'week_day'):
                data[key] = request.data[key]
                if(key == 'open_time'):
                    data[key] = datetime.strptime(request.data[key], '%H:%M:%S')
                if(key == 'close_time'):
                    data[key] = datetime.strptime(request.data[key], '%H:%M:%S')

        
        b = Bathrooms.objects.filter(id = bathroom_id)
        day = DayAvailable.objects.get(week_day = week_day, bathroom_id = b[0])

        if(b[0].address_id.user.username == user.username):
            updateThis = TimesAvailable.objects.filter(week_day = day, open_time = old_open_time)
            updateThis.update(**data)
            
            timeSlot = TimesAvailable.objects.filter(week_day = day, open_time = data['open_time'])
            serializer = TimesAvailable_Serializer(timeSlot[0], many = False)

            return JsonResponse(serializer.data, safe = False)

    except Token.DoesNotExist:
        return JsonResponse("Invalid Token", safe = False)

#Model Deletes
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@throttle_classes([UserRateThrottle])
def DeleteAddress(request):
    try:
        authToken = request.headers.get('Authorization')[6:]
        user = Token.objects.get(key = authToken).user

        a = Addresses.objects.get(id = int(request.data['id']), user = user)
        a.delete()

        return JsonResponse("Address successfully removed", safe = False)
    except Addresses.DoesNotExist:
        return JsonResponse("Address does not exist", safe = False)
    except Token.DoesNotExist:
        return JsonResponse("Invalid Token", safe = False)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@throttle_classes([UserRateThrottle])
def DeleteBathroom(request):
    try:
        authToken = request.headers.get('Authorization')[6:]
        user = Token.objects.get(key = authToken).user

        bathroom = Bathrooms.objects.get(id = int(request.data['id']))

        #Check to see if the user owns the bathroom
        if(user.username == bathroom.address_id.user.username):
            bathroom.delete()
            return JsonResponse("Bathroom successfully removed", safe = False)
        else:
              return JsonResponse("How did you get here? You do not own this bathroom!", safe = False)
    except Token.DoesNotExist:
        return JsonResponse("Invalid Token", safe = False)
    except Addresses.DoesNotExist:
        return JsonResponse("Address does not exist", safe = False)
    except Bathrooms.DoesNotExist:
        return JsonResponse("Bathroom does not exist", safe = False)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@throttle_classes([UserRateThrottle])
def DeleteTimeSlot(request): #Request data requires week_day, bathroom_id, and open_time in HH:MM:SS format
    try:
        authToken = request.headers.get('Authorization')[6:]
        user = Token.objects.get(key = authToken).user

        bathroom = Bathrooms.objects.get(id = int(request.data['bathroom_id']))

        #Check to see if the user owns the bathroom
        if(user.username == bathroom.address_id.user.username):
            #Need to get weekday and associated opening time
            day = DayAvailable.objects.get(bathroom_id = bathroom, week_day = request.data['week_day'])
            times = TimesAvailable.objects.filter(week_day = day, open_time = datetime.strptime(request.data['open_time'], '%H:%M:%S'))
            times.delete()

            return JsonResponse("Time slot successfully removed", safe = False)
        else:
              return JsonResponse("How did you get here? You do not own this bathroom!", safe = False)

    except Token.DoesNotExist:
        return JsonResponse("Invalid Token", safe = False)
    except Bathrooms.DoesNotExist:
        return JsonResponse("Bathroom does not exist", safe = False)
    except TimesAvailable.DoesNotExist:
        return JsonResponse("Time slot does not exist", safe = False)
    except DayAvailable.DoesNotExist:
        return JsonResponse("For week_day, your options are Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday.", safe = False)
    