from django.contrib import admin
from .models import AcctIn5M, AcctOut5M

models =[AcctIn5M, AcctOut5M]
admin.site.register(models)