from django.shortcuts import render
from .models import AcctIn1D, AcctOut1D, AcctIn5M, AcctOut5M, FlowQuerySets
from chartit import DataPool, Chart
from django.http import  HttpResponseNotFound

def home(request):
    return render(request, 'flow/base.html')

    
def top_incoming(request, pk):
    if pk == "1":
        top_ip_in      = AcctIn5M.objects.top_ip_in(pk)
        top_proto_in   = AcctIn5M.objects.top_proto(pk)  
        top_app_in     = AcctIn5M.objects.top_app_in(pk)
        top_packets_in = AcctIn5M.objects.top_packets_in(pk)
    elif pk == "6":
        top_ip_in      = AcctIn5M.objects.top_ip_in(pk)
        top_proto_in   = AcctIn5M.objects.top_proto(pk)  
        top_app_in     = AcctIn5M.objects.top_app_in(pk)
        top_packets_in = AcctIn5M.objects.top_packets_in(pk)     
    elif pk == "24":
        top_ip_in      = AcctIn5M.objects.top_ip_in(pk)
        top_proto_in   = AcctIn5M.objects.top_proto(pk)  
        top_app_in     = AcctIn5M.objects.top_app_in(pk)
        top_packets_in = AcctIn5M.objects.top_packets_in(pk) 
    else: 
        return   HttpResponseNotFound('<h1>Page not found</h1>')

    #Step 1: Create a DataPool with the data we want to retrieve.
    top_ip_in_ds = DataPool(series=[{'options': {
    		'source': top_ip_in,
    		},
            'terms': ['traffic', 'ip_dst' ]}])

    top_proto_in_ds = DataPool(series=[{'options': {
        'source': top_proto_in,
        },
        'terms': ['traffic', 'ip_proto' ]}])

    top_app_in_ds = DataPool(series=[{'options': {
        'source': top_app_in,
        },
        'terms': ['traffic', 'dst_port' ]}])

    top_packets_in_ds = DataPool(series=[{'options': {
        'source': top_packets_in,
        },
        'terms': ['sum_packets', 'ip_dst' ]}])
    #Step 2: Create the Chart object
    top_ip_in_chart = Chart(
            datasource = top_ip_in_ds,
            series_options =[{'options':{'type': 'pie',
                'allowPointSelect' : True, 'cursor' : 'pointer',
                'showInLegend': True,
                'dataLabels':{'enabled': False}},
                'terms':{'ip_dst': ['traffic']}}],
            chart_options = {
                'tooltip': {
                    'pointFormat' : '{series.name} : <b>{point.percentage:.1f}%</b>'},
                'title': {
                   'text': 'Top 10 Incoming Destinations'}})
    top_proto_in_chart = Chart(
            datasource = top_proto_in_ds,
            series_options =[{'options':{'type': 'pie',
                'allowPointSelect' : True, 'cursor' : 'pointer',
                'showInLegend': True, 'dataLabels':{'enabled': False}},
                'terms':{'ip_proto': ['traffic']}}],
            chart_options = {
                'tooltip': {
                    'pointFormat' : '{series.name} : <b>{point.percentage:.1f}%</b>'},
                'title': {
                   'text': 'Top 10 Incoming IP Protocols'}})
    top_app_in_chart = Chart(
            datasource = top_app_in_ds,
            series_options =[{'options':{'type': 'pie',
                'allowPointSelect' : True, 'cursor' : 'pointer',
                'showInLegend': True, 'dataLabels':{'enabled': False}},
                'terms':{'dst_port': ['traffic']}}],
            chart_options ={
                    'tooltip': {
                        'pointFormat' : '{series.name} : <b>{point.percentage:.1f}%</b>'},
                    'title': {
                        'text': 'Top 10 Incoming Applications'}})

    top_packets_in_chart = Chart(
            datasource = top_packets_in_ds,
            series_options =[{'options':{'type': 'pie',
                'allowPointSelect' : True, 'cursor' : 'pointer',
                'showInLegend': True, 'dataLabels':{'enabled': False}},
                'terms':{'ip_dst': ['sum_packets']}}],
            chart_options =
              {'title': {
                   'text': 'Top 10 Incoming Packets'}})
    return render (request, 'flow/top_incoming.html', {
        'top_ip_in': top_ip_in, 
        'top_proto_in': top_proto_in,
        'top_app_in' : top_app_in,
        'top_packets_in' : top_packets_in,
        'charts': [top_ip_in_chart, top_proto_in_chart, top_app_in_chart, top_packets_in_chart]})



def top_outgoing(request, pk):
    if pk == "1":
        top_ip_out      = AcctOut5M.objects.top_ip_out(pk)
        top_proto_out   = AcctOut5M.objects.top_proto(pk)  
        top_app_out     = AcctOut5M.objects.top_app_out(pk)
        top_packets_out = AcctOut5M.objects.top_packets_out(pk)
    elif pk == "6":
        top_ip_out     = AcctOut5M.objects.top_ip_out(pk)
        top_proto_out   = AcctOut5M.objects.top_proto(pk)  
        top_app_out     = AcctOut5M.objects.top_app_out(pk)
        top_packets_out = AcctOut5M.objects.top_packets_out(pk)     
    elif pk == "24":
        top_ip_out      = AcctOut5M.objects.top_ip_out(pk)
        top_proto_out   = AcctOut5M.objects.top_proto(pk)  
        top_app_out     = AcctOut5M.objects.top_app_out(pk)
        top_packets_out = AcctOut5M.objects.top_packets_iout(pk) 
    else: 
        return  HttpResponseNotFound('<h1>Page not found</h1>')   

    #Step 1: Create a DataPool with the data we want to retrieve.
    top_ip_out_ds = DataPool(series=[{'options': {
            'source': top_ip_out,
            },
            'terms': ['traffic', 'ip_src' ]}])
     #Step 2: Create the Chart object
    top_ip_out_chart = Chart(
            datasource = top_ip_out_ds,
            series_options =[{'options':{'type': 'pie',
                'allowPointSelect' : True, 'cursor' : 'pointer',
                'showInLegend': True,
                'dataLabels':{'enabled': False}},
                'terms':{'ip_src': ['traffic']}}],
            chart_options = {
                'tooltip': {
                    'pointFormat' : '{series.name} : <b>{point.percentage:.1f}%</b>'},
                'title': {
                   'text': 'Top 10 Source Locations Out'}})

    return render (request, 'flow/top_outgoing.html', {'top_ip_out': top_ip_out,
            'top_ip_out_chart': top_ip_out_chart})