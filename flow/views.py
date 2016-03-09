from django.shortcuts import render, render_to_response
from .models import AcctIn1D, AcctOut1D, AcctIn5M, AcctOut5M, FlowQuerySets
from chartit import DataPool, Chart
from django.http import  HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import ShowDataForm
from django.db.models import Sum

@login_required
def home(request):
    return render(request, 'flow/base.html')

@login_required   
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
@login_required
def top_outgoing(request, pk):
    if pk == "1":
        top_ip_out      = AcctOut5M.objects.top_ip_out(pk)
        top_proto_out   = AcctOut5M.objects.top_proto(pk)  
        top_app_out     = AcctOut5M.objects.top_app_out(pk)
        top_packets_out = AcctOut5M.objects.top_packets_out(pk)
    elif pk == "6":
        top_ip_out      = AcctOut5M.objects.top_ip_out(pk)
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
    return render (request, 'flow/top_outgoing.html', {
                'top_ip_out': top_ip_out, 
                'top_proto_out': top_proto_out,
                'top_app_out' : top_app_out,
                'top_packets_out' : top_packets_out,
                'charts': [top_ip_out_chart, top_proto_out_chart, top_app_out_chart, top_packets_out_chart]})
@login_required
def traffic_all(request):
    traffic_in = AcctIn1D.objects.traffic_in()
    traffic_out = AcctOut1D.objects.traffic_out()
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
                        'time_out' : ['traffic']}
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
    return  render(request, 'flow/traffic.html', {
                'charts': [traffic_in_chart, traffic_out_chart]
                })

def export_data(request):   
    res = None
    form = None

    if request.method == 'POST':
        form = ShowDataForm(request.POST or None)
        request.session['Submit'] = request.POST
        # check whether it's valid:
        if form.is_valid():
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')   
            choose_field = form.cleaned_data.get('choice')

            if 'Incoming' in choose_field:
                res = AcctIn1D.objects.values('ip_dst')
            else:
                res = AcctOut1D.objects.values('ip_src')

            if not 'checkbox' in request.POST:
                address = form.cleaned_data.get('address')
                res = res.filter(ip_dst = address)
        
            res = res.filter(stamp_updated__gte=start_date,
                             stamp_updated__lte=end_date)\
                            .annotate(traffic=Sum('bytes'))\
                            .order_by('-traffic')[:500]
#    if request.method == 'POST':
#        form = ShowDataForm(request.POST or None)
#        request.session['Submit'] = request.POST
#        # check whether it's valid:
#        if form.is_valid():
#            start_date = form.cleaned_data.get('start_date')
#            end_date = form.cleaned_data.get('end_date')   
#            
#
#            res = AcctIn1D.objects.values('ip_dst')
#            if not 'checkbox' in request.POST:
#                address = form.cleaned_data.get('address')
#                res = res.filter(ip_dst = address)
#        
#            res = res.filter(stamp_updated__gte=start_date,
#                             stamp_updated__lte=end_date)\
#                            .annotate(traffic=Sum('bytes'))\
#                            .order_by('-traffic')
    else:
        form = ShowDataForm()


    return render(request, 'flow/export.html',
                    {
                       'form' : form,
                       'res'  : res,
                    })

#def listing(request, queryset):
#    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#    page = request.GET.get('page')
#    paginator = Paginator(res, 25)
#
#    try:
#        queryset = paginator.page(page)
#    except PageNotAnInteger:
#        # If page is not an integer, deliver first page.
#        queryset = paginator.page(1)
#    except EmptyPage:
#        # If page is out of range (e.g. 9999), deliver last page of results.
#        queryset = paginator.page(paginator.num_pages)
#
#
#        return queryset
#def download_workbook(request, query):
#
#    from django.http.response import HttpResponse
#    queryset = query
#    columns = (
#        'ip_dst',
#        'bytes' )
#    workbook = queryset_to_workbook(queryset, columns)
#    response = HttpResponse(content_type='application/vnd.ms-excel')
#    response['Content-Disposition'] = 'attachment; filename="export.xls"'
#    workbook.save(response)
#    return response


#def WriteToExcel(queryset):
#    from django.http.response import HttpResponse
#    from io import BytesIO
#    from xlsxwriter.workbook import Workbook
#    
#    output = BytesIO()
#
#
#    # initialises list object
#    a_list = []
#
#    for g in queryset:  
#        a_list.append({'obj': g})
#
#    """sorts the data in the list  by the attribute named 'attribute'
#    , and sorts it in reverse"""
#
#
#    data = sorted(a_list, key=lambda k: k['obj'].attribute, reverse=True)
#
#
#    # Create a workbook and add a worksheet.
#    workbook = Workbook(output)
#    worksheet = workbook.add_worksheet('Report')
#    
#    # Add a bold format to use to highlight cells.
#    bold = workbook.add_format({'bold': True})
#    
#    # Write some data headers.
#    worksheet.write('A1', 'Destination IP', bold)
#    worksheet.write('B1', 'Traffic', bold)
#    
#    # Iterate over the data and write it out row by row.
#    for i, row in enumerate(data):
#    
#        """for each object in the date list, attribute1 & attribute2
#        are written to the first & second column respectively,
#        for the relevant row. The 3rd arg is a failure message if
#        there is no data available"""
#    
#        worksheet.write(i, 0, getattr(row['obj'], 'attribute1', 'attribute1 not available'))
#        worksheet.write(i, 1, getattr(row['obj'], 'attribute2', 'attribute2 not available'))
#    
#    # closes the workbook
#    workbook.close()
#    response = HttpResponse(output.read(),content_type='application/vnd.ms-excel')
#    response['Content-Disposition'] = 'attachment; filename=Report.xlsx'
#
##   response.write(xls_data)
#    return response