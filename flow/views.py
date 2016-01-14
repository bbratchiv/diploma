from django.shortcuts import render
from django.utils import timezone
from .models import Flow
from chartit import DataPool, Chart
# Create your views here.


def top_conversations(request):
    top_con = Flow.objects.raw('SELECT id, ip_src, ip_dst, src_port, ip_proto, sum(bytes) as Traffic FROM acct GROUP BY ip_src, ip_dst, ip_proto ORDER BY 6 DESC limit 10;') 
    return render (request, 'flow/home.html', {'top_con': top_con })

