from django.contrib import admin
#from django.contrib.auth.admin import UserAdmin
from Air_PnP.models import Users
from Air_PnP.models import Bathrooms
#Register your models here.
#class MyUserAdmin(UserAdmin):

admin.site.register(Users)
admin.site.register(Bathrooms)

