from django.shortcuts import render, render_to_response
from .models import  *
from chartit import DataPool, Chart
from django.http import  HttpResponseNotFound, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import *
from django.db.models import Sum, Count
from datetime import datetime, timedelta
from django.apps import apps
from django.db import models
import copy

hour = datetime.now() - timedelta(hours=1)
_3hours = datetime.now() - timedelta(hours=3)
_6hours = datetime.now() - timedelta(hours=6)
_12hours = datetime.now() - timedelta(hours=12)
_24hours = datetime.now() - timedelta(hours=24)
week = datetime.now() - timedelta(weeks=1)
month = datetime.now() - timedelta(days=30)


@login_required
def home(request):
    form1 = SelectDeviceForm()
    form2 = AddDeviceForm()
    form3 = RemoveDeviceForm()

    devices = Devices.objects.all()
    
    if 'Select Device' in request.POST:
        form1 = SelectDeviceForm(request.POST)
        if form1.is_valid():
            request.session['devices'] = form1.cleaned_data.get('device_name')

    elif 'Add Device' in request.POST: 
        form2 = AddDeviceForm(request.POST)
        # check whether it's valid:
        if form2.is_valid(): 
            device = form2.save(commit = False)
            device.save()
            return HttpResponseRedirect("/home/")

    elif 'Remove Device' in request.POST:
        form3 = RemoveDeviceForm(request.POST)
        if form3.is_valid():
            Devices.objects.filter(device_id = request.POST['device_name']).delete()
            if 'checkbox' in request.POST:
                TrafficIn.objects.filter(peer_ip_src = request.session['devices']).delete()
                TrafficOut.objects.filter(peer_ip_src = request.session['devices']).delete()


    return render(request, 'flow/home.html', {'selectDevice' : form1,
                             'addDevice' : form2, 'removeDevice' : form3,
                                 'devices': devices })

@login_required   
def top_incoming(request, pk):
    if 'devices' not in request.session:
        return HttpResponse("<p>Please select device at <a href='/home/'>start page</a></p>")

    if pk =="0" or pk =="1" or pk =="6" or pk =="24":
        top_ip_in      = TrafficIn.objects.top_ip_in(pk, request.session['devices'])
        top_proto_in   = TrafficIn.objects.top_proto_in(pk, request.session['devices'])  
        top_app_in     = TrafficIn.objects.top_app_in(pk, request.session['devices'])
        top_packets_in = TrafficIn.objects.top_packets_in(pk, request.session['devices'])
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
                'chart' : {
                    'backgroundColor' : '#909191',
                    'borderRadius' : '20'},           
                'tooltip': {
                    'pointFormat' : '{series.name} : <b>{point.percentage:.1f}%</b>'},
                'title': {
                   'text': 'Top 10 Incoming Destinations',
                    'style':{'color':'white'}}
            })
    top_proto_in_chart = Chart(
            datasource = top_proto_in_ds,
            series_options =[{'options':{'type': 'pie',
                'allowPointSelect' : True, 'cursor' : 'pointer',
                'showInLegend': True, 'dataLabels':{'enabled': False}},
                'terms':{'ip_proto': ['traffic']}}],
            chart_options = {
                'chart' : {
                    'backgroundColor' : '#909191',
                    'borderRadius' : '20'},
                'tooltip': {
                    'pointFormat' : '{series.name} : <b>{point.percentage:.1f}%</b>'},
                'title': {
                   'text': 'Top 10 Incoming IP Protocols',
                    'style':{'color':'white'}}
            })
    top_app_in_chart = Chart(
            datasource = top_app_in_ds,
            series_options =[{'options':{'type': 'pie',
                'allowPointSelect' : True, 'cursor' : 'pointer',
                'showInLegend': True, 'dataLabels':{'enabled': False}},
                'terms':{'dst_port': ['traffic']}}],
            chart_options ={
                    'chart' : {
                        'backgroundColor' : '#909191',
                        'borderRadius' : '20'},
                    'tooltip': {
                        'pointFormat' : '{series.name} : <b>{point.percentage:.1f}%</b>'},
                    'title': {
                        'text': 'Top 10 Incoming Applications',
                        'style':{'color':'white'}}
            })
    top_packets_in_chart = Chart(
            datasource = top_packets_in_ds,
            series_options =[{'options':{'type': 'pie',
                'allowPointSelect' : True, 'cursor' : 'pointer',
                'showInLegend': True, 'dataLabels':{'enabled': False}},
                'terms':{'ip_dst': ['sum_packets']}}],
            chart_options = {
                'chart' : {
                    'backgroundColor' : '#909191',
                    'borderRadius' : '20'},
                'title': {
                   'text': 'Top 10 Incoming Packets',
                    'style':{'color':'white'}}
            })

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

    if pk =="0" or pk =="1" or pk =="6" or pk =="24":
        top_ip_out      = TrafficOut.objects.top_ip_out(pk, request.session['devices'])
        top_proto_out   = TrafficOut.objects.top_proto_out(pk, request.session['devices'])  
        top_app_out     = TrafficOut.objects.top_app_out(pk, request.session['devices'])
        top_packets_out = TrafficOut.objects.top_packets_out(pk, request.session['devices'])
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
                'chart' : {
                    'backgroundColor' : '#909191',
                    'borderRadius' : '20'},
                'tooltip': {
                    'pointFormat' : '{series.name} : <b>{point.percentage:.1f}%</b>'},
                'title': {
                   'text': 'Top 10 Source Locations Out',
                   'style':{'color':'white'}}
            })

    top_proto_out_chart = Chart(
            datasource = top_proto_out_ds,
            series_options =[{'options':{'type': 'pie',
                'allowPointSelect' : True, 'cursor' : 'pointer',
                'showInLegend': True, 'dataLabels':{'enabled': False}},
                'terms':{'ip_proto': ['traffic']}}],
            chart_options = {
                'chart' : {
                    'backgroundColor' : '#909191',
                    'borderRadius' : '20'},
                'tooltip': {
                    'pointFormat' : '{series.name} : <b>{point.percentage:.1f}%</b>'},
                'title': {
                   'text': 'Top 10 Outgoing IP Protocols',
                   'style':{'color':'white'}}
            })
    top_app_out_chart = Chart(
            datasource = top_app_out_ds,
            series_options =[{'options':{'type': 'pie',
                'allowPointSelect' : True, 'cursor' : 'pointer',
                'showInLegend': True, 'dataLabels':{'enabled': False}},
                'terms':{'src_port': ['traffic']}}],
            chart_options ={
                    'chart' : {
                        'backgroundColor' : '#909191',
                        'borderRadius' : '20'},
                    'tooltip': {
                        'pointFormat' : '{series.name} : <b>{point.percentage:.1f}%</b>'},
                    'title': {
                        'text': 'Top 10 Outgoing Applications',
                        'style':{'color':'white'}}
            })

    top_packets_out_chart = Chart(
            datasource = top_packets_out_ds,
            series_options =[{'options':{'type': 'pie',
                'allowPointSelect' : True, 'cursor' : 'pointer',
                'showInLegend': True, 'dataLabels':{'enabled': False}},
                'terms':{'ip_src': ['sum_packets']}}],
            chart_options = {
                'chart' : {
                    'backgroundColor' : '#909191',
                    'borderRadius' : '20'},
                'title': {
                   'text': 'Top 10 Incoming Packets',
                    'style':{'color':'white'}}
            })


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

 
    traffic_in = TrafficIn.objects.traffic(request.session['devices'])
    traffic_out = TrafficOut.objects.traffic(request.session['devices'])

    
    #Step 1: Create a DataPool with the data we want to retrieve.
    traffic_in_ds = DataPool(
        series=[{'options': {
            'source': traffic_in},
            'terms': [
            'traffic', {'time_in' : 'stamp_updated'}]
            }]
            )

    traffic_out_ds = DataPool(
            series=[{'options': {
        'source' : traffic_out},
            'terms': [
            'traffic', {'time_out':'stamp_updated'}]
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
                        'time_in' : ['traffic']}
                  }],
                  chart_options = {
                    'title' : {
                       'text' : 'Incoming Traffic Chart',
                       'style':{'color':'white'}},
                    'subtitle' : {
                        'text': 'Click and drag to zoom in. Hold down shift key to pan.',
                        'style':{'color':'white'}},
                    'chart' : {
                        'backgroundColor' : '#909191',
                        'borderRadius' : '20',
                        'zoomType' : 'x',
                        'panning' : {'enabled' : True},
                        'panKey' : 'shift'},
                    'xAxis' : {
                        'title' : {'text' : 'Date time',
                        'style':{'color':'white'}},
                        'labels' : {
                            'style':{'color':'white'}}},
                    'yAxis' : {
                        'title' : {'text' : 'Traffic',
                        'style':{'color':'white'}},
                        'labels' : {
                            'style':{'color':'white'}}
                       }}
                    )   

    traffic_out_chart = Chart(
                datasource = traffic_out_ds,
                series_options = 
                 [{'options': {
                     'type' : 'line', 'stacking': False,
                     'showInLegend': False},
                    'terms': {
                        'time_out' : ['traffic']}
                  }],
                  chart_options ={
                    'title' : {
                       'text' : 'Outgoing Traffic Chart',
                       'style':{'color':'white'}},
                    'subtitle' : {
                        'text': 'Click and drag to zoom in. Hold down shift key to pan.',
                        'style':{'color':'white'}},
                    'chart' : {
                        'backgroundColor' : '#909191',
                        'borderRadius' : '20',
                        'zoomType' : 'x',
                        'panning' : {'enabled' : True},
                        'panKey' : 'shift'},
                    'xAxis' : {
                        'title' : {'text' : 'Date time',
                        'style':{'color':'white'}},
                        'labels' : {
                            'style':{'color':'white'}}},
                    'yAxis' : {
                        'title' : {'text' : 'Traffic',
                        'style':{'color':'white'}},
                        'labels' : {
                            'style':{'color':'white'}}
                       }}
                    )   
  
    return  render(request, 'flow/traffic.html', {
                'charts': [traffic_in_chart, traffic_out_chart]
                })

@login_required
def traffic_report(request):   
    res = None
    form = None
    sum1 = None #for summing traffic
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
                res = TrafficIn.objects.values('ip_dst').filter(peer_ip_src=request.session['devices'])
            else:
                res = TrafficOut.objects.values('ip_src').filter(peer_ip_src=request.session['devices'])

            if 'address' in request.POST and 'Incoming' in traffic_type :
                res = res.filter(ip_dst = address)
            elif 'address' in request.POST and 'Outgoing' in traffic_type :
                res = res.filter(ip_src = address)
        
            if 'one' in time_range:
                res = res.filter(stamp_updated__gt = hour)
            elif 'three' in time_range:
                res = res.filter(stamp_updated__gt= _3hours)
            elif 'six' in time_range:
                res = res.filter(stamp_updated__gt= _6hours)
            elif 'twelve' in time_range:
                res = res.filter(stamp_updated__gt= _12hours)
            elif 'twentyfour' in time_range:
                res = res.filter(stamp_updated__gt= _24hours)
            elif 'week' in time_range:
                res = res.filter(stamp_updated__gt= week)
            elif 'month' in time_range:
                res = res.filter(stamp_updated__gt= month)
            elif 'custom' in time_range:
                start_date = form.cleaned_data.get('start_date')
                end_date = form.cleaned_data.get('end_date')
                res = res.filter(stamp_updated__gte=start_date,
                                stamp_updated__lte=end_date)

            res = res.annotate(traffic=Sum('bytes'))\
                            .order_by('-traffic')
            sum1 = res.aggregate(Sum('traffic'))
    else:
        form = TrafficReport()


    return render(request, 'flow/traffic_report.html',
                    {
                       'form' : form,
                       'res'  : res,
                       'sum1' : sum1
                    })

@login_required
def custom_report(request):   
    res = None
    form = None
    sum2 = None # for summing traffic

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
                res = TrafficIn.objects.values('ip_dst', 'dst_port', 'ip_proto', 'stamp_updated')\
                                                .filter(peer_ip_src=request.session['devices'])
            else: 
                res = TrafficOut.objects.values('ip_src', 'src_port', 'ip_proto', 'stamp_updated')\
                                                .filter(peer_ip_src=request.session['devices'])

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
            
            if 'one' in time_range:
                res = res.filter(stamp_updated__gte = hour)
            elif 'three' in time_range:
                res = res.filter(stamp_updated__gte= _3hours)
            elif 'six' in time_range:
                res = res.filter(stamp_updated__gte= _6hours)
            elif 'twelve' in time_range:
                res = res.filter(stamp_updated__gte= _12hours)
            elif 'twentyfour' in time_range:
                res = res.filter(stamp_updated__gte= _24hours)
            elif 'week' in time_range:
                res = res.filter(stamp_updated__gte= week)
            elif 'month' in time_range:
                res = res.filter(stamp_updated__gte= month)
            elif 'custom' in time_range:
                start_date = form.cleaned_data.get('start_date')
                end_date = form.cleaned_data.get('end_date')
                res = res.filter(stamp_updated__gte=start_date,
                                stamp_updated__lte=end_date)

            res = res.annotate(traffic=Sum('bytes'))\
                            .order_by('-traffic')
            sum2 = res.aggregate(Sum('traffic'))

            
    else:
        form = CustomReport()

    return render (request, 'flow/custom_report.html',
                {
                    'form1' : form,
                    'res1' : res,
                    'sum2' : sum2
                })

@login_required
def billing(request):
    res = None
    billing_rate = None
    sum3 = None

#    if 'devices' not in request.session:
#        return HttpResponse("<p>Please select device at <a href='/home/'>start page</a></p>")


    form = AddBillingForm()
    form2 = RemoveBillingForm()
    form3 = CalculateBillingForm()
    form4 = ChangeDeviceBillingForm()
    if 'Add Billing' in request.POST: 
        form = AddBillingForm(request.POST)
        # check whether it's valid:
        if form.is_valid(): 
            billing = form.save(commit = False)
            billing.save()
            return HttpResponseRedirect("/billing/")

    elif 'Delete Billing' in request.POST:
        form2 = RemoveBillingForm(request.POST)
        if form2.is_valid():
            Billing.objects.filter(billing_id = request.POST['rate_name']).delete()


    elif 'Change Billing' in request.POST:
        device = Devices.objects.get(device_id = request.POST['device_name'])
        billing = Billing.objects.get(billing_id = request.POST['billing'])
        device.billing = billing
        device.save()

    elif "Calculate Billing" in request.POST:
        form3 = CalculateBillingForm(request.POST)
        if form3.is_valid():
            device_name = form3.cleaned_data.get('device_name')
            traffic_type = form3.cleaned_data.get('traffic_type')
            address = form3.cleaned_data.get('address')
            time_range = form3.cleaned_data.get('time_range')

            if 'Incoming' in traffic_type:
                res = TrafficIn.objects.values('ip_dst').filter(peer_ip_src=device_name)
            else:
                res = TrafficOut.objects.values('ip_src').filter(peer_ip_src=device_name)

            if 'address' in request.POST and 'Incoming' in traffic_type :
                res = res.filter(ip_dst = address)
            elif 'address' in request.POST and 'Outgoing' in traffic_type :
                res = res.filter(ip_src = address)
            
            if 'one' in time_range:
                res = res.filter(stamp_updated__gt = hour)
            elif 'three' in time_range:
                res = res.filter(stamp_updated__gt= _3hours)
            elif 'six' in time_range:
                res = res.filter(stamp_updated__gt= _6hours)
            elif 'twelve' in time_range:
                res = res.filter(stamp_updated__gt= _12hours)
            elif 'twentyfour' in time_range:
                res = res.filter(stamp_updated__gt= _24hours)
            elif 'week' in time_range:
                res = res.filter(stamp_updated__gt= week)
            elif 'month' in time_range:
                res = res.filter(stamp_updated__gt= month)
            elif 'custom' in time_range:
                start_date = form3.cleaned_data.get('start_date')
                end_date = form3.cleaned_data.get('end_date')
                res = res.filter(stamp_updated__gte=start_date,
                                stamp_updated__lte=end_date)
            
            res = res.annotate(traffic=Sum('bytes'))
            res = res.annotate(_traffic=Sum('bytes'))\
                            .order_by('-traffic')   

            sum3 = res.aggregate(Sum('traffic'))
            
            #  modifying traffic field calculating traffic cost
            billing_id = Devices.objects.values("billing_id").filter(device_ip=request.session['devices'])
            cost_rate_coef = Billing.objects.values("cost_rate").filter(billing_id__in=billing_id)  


            for i in res:
                for j in cost_rate_coef:
                    #if device has no 'cost_rate' field it's not billable
                    if not j['cost_rate']:
                        res = 'Not billable'
                        break
                    elif i['_traffic']:
                        i['_traffic'] = round(i['_traffic'] * (j['cost_rate']/1073741824), 4) 


    return render(request, 'flow/billing.html', {'addBilling' : form, 'removeBilling' : form2,
                            'calculateBilling' : form3, 'changeBilling' : form4,
                            'res' : res, 'sum3' : sum3})

