from django.shortcuts import render, render_to_response
from .models import  FlowQuerySets, Devices, Device1_In, Device1_Out, Device2_In, Device2_Out
from chartit import DataPool, Chart
from django.http import  HttpResponseNotFound, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import TrafficReport, CustomReport, SelectDeviceForm 
from django.db.models import Sum
from datetime import datetime, timedelta
from django.apps import apps
from django.db import models



hour = datetime.now() - timedelta(hours=1)
hours3 = datetime.now() - timedelta(hours=3)
hours6 = datetime.now() - timedelta(hours=6)
hours12 = datetime.now() - timedelta(hours=12)
hours24 = datetime.now() - timedelta(days=1)
week = datetime.now() - timedelta(weeks=1)
month = datetime.now() - timedelta(days=30)
ModelIn = None
ModelOut = None

@login_required
def home(request):

    form1 = SelectDeviceForm()
#    form2 = AddDeviceForm()
    global ModelIn
    global ModelOut

    if request.method == 'POST' and 'Select Device':
        form1 = SelectDeviceForm(request.POST)
        if form1.is_valid():
            request.session['devices'] = form1.cleaned_data.get('device_name') 
            if request.session['devices'] == 'mikrotik':
                ModelIn = Device1_In
                ModelOut = Device1_Out
            elif request.session['devices'] == 'cisco':
                ModelIn = Device2_In
                ModelOut = Device2_Out

#    elif request.method == 'POST' and 'Add Device': 
#        form2 = AddDeviceForm(request.POST)
#        # check whether it's valid:
#        if form2.is_valid(): 
#            device = form2.save(commit = False)
#             # commit=False tells Django that "Don't send this to database yet.  
#            device.device_name = request.device_name
#            device.device_ip = request.device_ip
#            device.save()

    return render(request, 'flow/home.html', {'selectDevice' : form1,}) #'addDevice' : form2 })

@login_required   
def top_incoming(request, pk):
    if 'devices' not in request.session:
        return HttpResponse("<p>Please select device at <a href='/home/'>start page</a></p>")

    try:
        if pk == "0":
            top_ip_in      = ModelIn.objects.top_ip_in(pk)
            top_proto_in   = ModelIn.objects.top_proto(pk)  
            top_app_in     = ModelIn.objects.top_app_in(pk)
            top_packets_in = ModelIn.objects.top_packets_in(pk)
        elif pk == "1":
            top_ip_in      = ModelIn.objects.top_ip_in(pk)
            top_proto_in   = ModelIn.objects.top_proto(pk)  
            top_app_in     = ModelIn.objects.top_app_in(pk)
            top_packets_in = ModelIn.objects.top_packets_in(pk)
        elif pk == "6":
            top_ip_in      = ModelIn.objects.top_ip_in(pk)
            top_proto_in   = ModelIn.objects.top_proto(pk)  
            top_app_in     = ModelIn.objects.top_app_in(pk)
            top_packets_in = ModelIn.objects.top_packets_in(pk)     
        elif pk == "24":
            top_ip_in      = ModelIn.objects.top_ip_in(pk)
            top_proto_in   = ModelIn.objects.top_proto(pk)  
            top_app_in     = ModelIn.objects.top_app_in(pk)
            top_packets_in = ModelIn.objects.top_packets_in(pk) 
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
    except Exception as e: 
        print (e)
        #return HttpResponse("<p>Please select device at <a href='/home/'>start page</a></p>")
    return render (request, 'flow/top_incoming.html', {
        'top_ip_in': top_ip_in, 
        'top_proto_in': top_proto_in,
        'top_app_in' : top_app_in,
        'top_packets_in' : top_packets_in,
        'charts': [top_ip_in_chart, top_proto_in_chart, top_app_in_chart, top_packets_in_chart]})

@login_required
def top_outgoing(request, pk):
    if 'devices' not in request.session:
        return HttpResponse("<p>Please select device at <a href='/home/'>start page</a></p>")
    try:
        if pk == "0":
            top_ip_out      = ModelOut.objects.top_ip_out(pk)
            top_proto_out   = ModelOut.objects.top_proto(pk)  
            top_app_out     = ModelOut.objects.top_app_out(pk)
            top_packets_out = ModelOut.objects.top_packets_out(pk)
        elif pk == "1":
            top_ip_out      = ModelOut.objects.top_ip_out(pk)
            top_proto_out   = ModelOut.objects.top_proto(pk)  
            top_app_out     = ModelOut.objects.top_app_out(pk)
            top_packets_out = ModelOut.objects.top_packets_out(pk)
        elif pk == "6":
            top_ip_out      = ModelOut.objects.top_ip_out(pk)
            top_proto_out   = ModelOut.objects.top_proto(pk)  
            top_app_out     = ModelOut.objects.top_app_out(pk)
            top_packets_out = ModelOut.objects.top_packets_out(pk)     
        elif pk == "24":
            top_ip_out      = ModelOut.objects.top_ip_out(pk)
            top_proto_out   = ModelOut.objects.top_proto(pk)  
            top_app_out     = ModelOut.objects.top_app_out(pk)
            top_packets_out = ModelOut.objects.top_packets_out(pk) 
        else: 
            return  HttpResponseNotFound('<h1>Page not found</h1>')   

        #Step 1: Create a DataPool with the data we want to retrieve.
        top_ip_out_ds = DataPool(series=[{'options': {
                'source': top_ip_out,
                },
                'terms': ['traffic', 'ip_src' ]}])
        top_proto_out_ds = DataPool(series=[{'options': {
            'source': top_proto_out,
            },
            'terms': ['traffic', 'ip_proto' ]}])
    
        top_app_out_ds = DataPool(series=[{'options': {
            'source': top_app_out,
            },
            'terms': ['traffic', 'src_port' ]}])
    
        top_packets_out_ds = DataPool(series=[{'options': {
            'source': top_packets_out,
            },
            'terms': ['sum_packets', 'ip_src' ]}])
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
    
        top_proto_out_chart = Chart(
                datasource = top_proto_out_ds,
                series_options =[{'options':{'type': 'pie',
                    'allowPointSelect' : True, 'cursor' : 'pointer',
                    'showInLegend': True, 'dataLabels':{'enabled': False}},
                    'terms':{'ip_proto': ['traffic']}}],
                chart_options = {
                    'tooltip': {
                        'pointFormat' : '{series.name} : <b>{point.percentage:.1f}%</b>'},
                    'title': {
                       'text': 'Top 10 Outgoing IP Protocols'}})
        top_app_out_chart = Chart(
                datasource = top_app_out_ds,
                series_options =[{'options':{'type': 'pie',
                    'allowPointSelect' : True, 'cursor' : 'pointer',
                    'showInLegend': True, 'dataLabels':{'enabled': False}},
                    'terms':{'src_port': ['traffic']}}],
                chart_options ={
                        'tooltip': {
                            'pointFormat' : '{series.name} : <b>{point.percentage:.1f}%</b>'},
                        'title': {
                            'text': 'Top 10 Outgoing Applications'}})
    
        top_packets_out_chart = Chart(
                datasource = top_packets_out_ds,
                series_options =[{'options':{'type': 'pie',
                    'allowPointSelect' : True, 'cursor' : 'pointer',
                    'showInLegend': True, 'dataLabels':{'enabled': False}},
                    'terms':{'ip_src': ['sum_packets']}}],
                chart_options =
                  {'title': {
                       'text': 'Top 10 Incoming Packets'}})
    except Exception as e: 
        print (e)
        #return HttpResponse("<p>Please select device at <a href='/home/'>start page</a></p>")
    return render (request, 'flow/top_outgoing.html', {
                'top_ip_out': top_ip_out, 
                'top_proto_out': top_proto_out,
                'top_app_out' : top_app_out,
                'top_packets_out' : top_packets_out,
                'charts': [top_ip_out_chart, top_proto_out_chart, top_app_out_chart, top_packets_out_chart]})

@login_required
def traffic_all(request):

    if 'devices' not in request.session:
        return HttpResponse("<p>Please select device at <a href='/home/'>start page</a></p>")

 
    traffic_in = ModelIn.objects.traffic()
    traffic_out = ModelOut.objects.traffic()

    
    #Step 1: Create a DataPool with the data we want to retrieve.
    traffic_in_ds = DataPool(
        series=[{'options': {
            'source': traffic_in},
            'terms': [
            'bytes', {'time_in' : 'stamp_updated'}]
            }]
            )

    traffic_out_ds = DataPool(
            series=[{'options': {
        'source' : traffic_out},
            'terms': [
            'bytes', {'time_out':'stamp_updated'}]
            }]
            )

    #Step 2: Create the Chart object
    traffic_in_chart = Chart(
                datasource = traffic_in_ds,
                series_options = 
                 [{'options': {
                     'type' : 'line', 'stacking': False,
                     'showInLegend': False},
                    'terms': {
                        'time_in' : ['bytes']}
                  }],
                  chart_options =
                  {'title' : {
                       'text' : 'Incoming Traffic Chart '},
                    'subtitle' : {
                        'text': 'Click and drag to zoom in. Hold down shift key to pan.'},
                    'chart' : {
                       'zoomType' : 'x',
                       'panning' : {'enabled' : True},
                       'panKey' : 'shift'},
                     'xAxis' : {
                       'title' : {'text' : 'Date time'}
                       }}
                    )   

    traffic_out_chart = Chart(
                datasource = traffic_out_ds,
                series_options = 
                 [{'options': {
                     'type' : 'line', 'stacking': False,
                     'showInLegend': False},
                    'terms': {
                        'time_out' : ['bytes']}
                  }],
                  chart_options =
                  {'title' : {
                       'text' : 'Outgoing Traffic Chart '},
                    'subtitle' : {
                        'text': 'Click and drag to zoom in. Hold down shift key to pan.'},
                    'chart' : {
                       'zoomType' : 'x',
                       'panning' : {'enabled' : True},
                       'panKey' : 'shift'},
                     'xAxis' : {
                       'title' : {'text' : 'Date time'}
                       }}
                    )  
#    except Exception as e: 
#        print (e)
        #return HttpResponse("<p>Please select device at <a href='/home/'>start page</a></p>")    
    return  render(request, 'flow/traffic.html', {
                'charts': [traffic_in_chart, traffic_out_chart]
                })

@login_required
def traffic_report(request):   
    res = None
    form = None
    if 'devices' not in request.session:
        return HttpResponse("<p>Please select device at <a href='/home/'>start page</a></p>")

    if request.method == 'POST':
        form = TrafficReport(request.POST or None)
        # check whether it's valid:
        if form.is_valid(): 
            traffic_type = form.cleaned_data.get('traffic_type')
            address = form.cleaned_data.get('address')
            time_range = form.cleaned_data.get('time_range')

            if 'Incoming' in traffic_type:
                res = ModelIn.objects.values('ip_dst')
            else:
                res = ModelOut.objects.values('ip_src')

            if 'address' in request.POST and 'Incoming' in traffic_type :
                res = res.filter(ip_dst = address)
            elif 'address' in request.POST and 'Outgoing' in traffic_type :
                res = res.filter(ip_src = address)
        
            if 'hour' in time_range:
                res = res.filter(stamp_updated__gte = hour)
            elif '3hours' in time_range:
                res = res.filter(stamp_updated__gte= hours3)
            elif '6hours' in time_range:
                res = res.filter(stamp_updated__gte= hours6)
            elif '12hours' in time_range:
                res = res.filter(stamp_updated__gte= hours12)
            elif '24hours' in time_range:
                res = res.filter(stamp_updated__gte= hours24)
            elif 'week' in time_range:
                res = res.filter(stamp_updated__gte= week)
            if 'month' in time_range:
                res = res.filter(stamp_updated__gte= month)
            elif 'custom' in time_range:
                start_date = form.cleaned_data.get('start_date')
                end_date = form.cleaned_data.get('end_date')
                res = res.filter(stamp_updated__gte=start_date,
                                stamp_updated__lte=end_date)

            res = res.annotate(traffic=Sum('bytes'))\
                            .order_by('-traffic')[:500]
    else:
        form = TrafficReport()


    return render(request, 'flow/traffic_report.html',
                    {
                       'form' : form,
                       'res'  : res,
                    })

@login_required
def custom_report(request):   
    res = None
    form = None

    if 'devices' not in request.session:
        return HttpResponse("<p>Please select device at <a href='/home/'>start page</a></p>")

    if request.method == 'POST':
        form = CustomReport(request.POST)
        # check whether it's valid:
        if form.is_valid():
            choice_criteria = form.cleaned_data.get('choice_criteria')
            traffic_type = form.cleaned_data.get('traffic_type')
            time_range = form.cleaned_data.get('time_range')

            if "Incoming" in traffic_type:
                res = ModelIn.objects.values('ip_dst', 'dst_port', 'ip_proto', 'bytes', 'stamp_updated')
            else: 
                res = ModelOut.objects.values('ip_src', 'src_port', 'ip_proto', 'bytes', 'stamp_updated')

            if 'source_ip' in choice_criteria:
                src_addr = form.cleaned_data.get('src_addr')
                res = res.filter(ip_src = src_addr)
            elif 'dest_ip' in choice_criteria:
                dst_addr = form.cleaned_data.get('dst_addr')
                res = res.filter(ip_dst = dst_addr)
            
            if choice_criteria == 'port1' and 'Incoming' in traffic_type:
                port = form.cleaned_data.get('port')
                res = res.filter(dst_port = port)
            elif choice_criteria == 'port1' and 'Outgoing' in traffic_type:
                port = form.cleaned_data.get('port')
                res = res.filter(src_port = port)
            
            if 'port_range' in choice_criteria and 'Incoming' in traffic_type:
                port_range1 = form.cleaned_data.get('pFrom')
                port_range2 = form.cleaned_data.get('pTo')
                res = res.filter(dst_port__gte = port_range1,
                                 dst_port__lte = port_range2)
            elif 'port_range' in choice_criteria and "Outgoing" in traffic_type:
                port_range1 = form.cleaned_data.get('pFrom')
                port_range2 = form.cleaned_data.get('pTo')
                res = res.filter(src_port__gte = port_range1,
                                 src_port__lte = port_range2)                
            
            if choice_criteria == 'protocol' :
                proto = form.cleaned_data.get('proto')
                res = res.filter(ip_proto = proto)
            
            if 'hour' in time_range:
                res = res.filter(stamp_updated__gte = hour)
            elif '3hours' in time_range:
                res = res.filter(stamp_updated__gte= hours3)
            elif '6hours' in time_range:
                res = res.filter(stamp_updated__gte= hours6)
            elif '12hours' in time_range:
                res = res.filter(stamp_updated__gte= hours12)
            elif '24hours' in time_range:
                res = res.filter(stamp_updated__gte= hours24)
            elif 'week' in time_range:
                res = res.filter(stamp_updated__gte= week)
            if 'month' in time_range:
                res = res.filter(stamp_updated__gte= month)
            elif 'custom' in time_range:
                start_date = form.cleaned_data.get('start_date')
                end_date = form.cleaned_data.get('end_date')
                res = res.filter(stamp_updated__gte=start_date,
                                stamp_updated__lte=end_date)

            
    else:
        form = CustomReport()

    return render (request, 'flow/custom_report.html',
                {
                    'form1' : form,
                    'res1' : res,
                })