from django.shortcuts import render
from .models import Flow, FlowQuerySets
from chartit import DataPool, Chart
import socket


def top_conversations_app(request):
    top_con = Flow.objects.top_con()
    top_proto = Flow.objects.top_proto()  
    top_app = Flow.objects.top_app()

    #Step 1: Create a DataPool with the data we want to retrieve.
    top_con_ds = DataPool(series=[{'options': {
    		'source': top_con,
    		},
            'terms': ['traffic', 'ip_src' ]}])

    top_proto_ds = DataPool(series=[{'options': {
        'source': top_proto,
        },
        'terms': ['traffic', 'ip_proto' ]}])

    top_app_ds = DataPool(series=[{'options': {
        'source': top_app,
        },
        'terms': ['traffic', 'dst_port' ]}])

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
                   'text': 'Top 10 IP Protocols'}})
    top_app_chart = Chart(
            datasource = top_app_ds,
            series_options =[{'options':{'type': 'pie','stacking': False},
                'terms':{'dst_port': ['traffic']}}],
            chart_options =
              {'title': {
                   'text': 'Top 10 Applications'}})

    return render (request, 'flow/home.html', {'top_con': top_con, 
        'top_proto': top_proto, 'top_app' : top_app,
        'charts': [top_con_chart, top_proto_chart, top_app_chart]})

