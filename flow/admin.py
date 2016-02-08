from django.contrib import admin
from .models import AcctIn1D, AcctOut1D, AcctIn5M, AcctOut5M

models =[AcctIn1D, AcctOut1D, AcctIn5M, AcctOut5M]
admin.site.register(models)