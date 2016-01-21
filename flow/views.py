from django.shortcuts import render
from django.utils import timezone
from .models import Flow
from chartit import DataPool, Chart
from django.db.models import Sum
import socket


def top_conversations_app(request):

    #top_con = Flow.objects.raw('SELECT id, ip_src, ip_dst, src_port, ip_proto, sum(bytes) as Traffic FROM acct GROUP BY ip_src, ip_dst, ip_proto ORDER BY 6 DESC limit 10;') 
    top_con = Flow.objects.values('ip_src', 'ip_dst', 'ip_proto').annotate(traffic=Sum('bytes')).order_by('-traffic')[:10]
    top_proto = Flow.objects.values('ip_proto').annotate(traffic=Sum('bytes')).order_by('-traffic')[:5]
    
    #Step 1: Create a DataPool with the data we want to retrieve.
    top_con_ds = DataPool(series=[{'options': {
    		'source': top_con,
    		},
            'terms': ['traffic', 'ip_src' ]}])

    top_proto_ds = DataPool(series=[{'options': {
        'source': top_proto,
        },
        'terms': ['traffic', 'ip_proto' ]}])

    #Step 2: Create the Chart object
    top_con_chart = Chart(
            datasource = top_con_ds,
            series_options =[{'options':{'type': 'pie','stacking': False},
                'terms':{'ip_src': ['traffic']}}],
            chart_options =
              {'title': {
                   'text': 'Top 10 Conversations'}})
    top_proto_chart = Chart(
            datasource = top_proto_ds,
            series_options =[{'options':{'type': 'pie','stacking': False},
                'terms':{'ip_proto': ['traffic']}}],
            chart_options =
              {'title': {
                   'text': 'Top 5 IP Protocols'}})

    return render (request, 'flow/home.html', {'top_con': top_con, 
        'charts': [top_con_chart, top_proto_chart], 'top_proto': top_proto})


def get_app (obj):
    for p in obj:
        return socket.getservbyport(p)