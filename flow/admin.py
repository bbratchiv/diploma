from django.contrib import admin
from .models import *
myModels = [TrafficIn, TrafficOut, Devices, Billing]
admin.site.register(myModels)