# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desidered behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from django.db.models import Sum
from datetime import datetime, timedelta

#>>> half_hour = datetime.now() - timedelta(hours=0.5)
#>>> AcctIn5M.objects.values('ip_dst', 'ip_proto').filter(stamp_updated__gt=half_hour).annotate(traffic=Sum('bytes')).order_by('-traffic')[:10]

hour = datetime.now() - timedelta(hours=1)
_6hours = datetime.now() - timedelta(hours=6)
_24hours = datetime.now() - timedelta(hours=24)

class FlowQuerySets(models.QuerySet):

    
    def top_ip_in(self, pk):
        queryset = self.values('ip_dst', 'ip_proto')
        if pk == "1":
            queryset = queryset.filter(stamp_updated__gt= hour)
        elif pk ==  "6":
            queryset = queryset.filter(stamp_updated__gt=_6hours)
        elif pk == "24":
            queryset = queryset.filter(stamp_updated__gt=_24hours)
        queryset = queryset.annotate(traffic=Sum('bytes')).order_by('-traffic')[:10]
        return queryset

    def top_ip_out(self, pk):
        queryset = self.values('ip_src', 'ip_proto')
        if pk == "1":
            queryset = queryset.filter(stamp_updated__gt=hour)
        elif pk == "6":
            queryset = queryset.filter(stamp_updated__gt=_6hours)
        elif pk =="24":
            queryset = queryset.filter(stamp_updated__gt=_24hours)
        queryset = queryset.annotate(traffic=Sum('bytes')).order_by('-traffic')[:10]
        return queryset

    def top_proto(self, pk): 
        queryset = self.values('ip_proto')
        if pk == "1":
            queryset = queryset.filter(stamp_updated__gt=hour)
        elif pk == "6":
            queryset = queryset.filter(stamp_updated__gt=_6hours)
        elif pk == "24":
            queryset = queryset.filter(stamp_updated__gt=_24hours)
        queryset = queryset.annotate(traffic=Sum('bytes')).order_by('-traffic')[:10]
        return queryset

    def top_packets_in(self, pk): 
        queryset = self.values('ip_dst')
        if pk =="1":
            queryset = queryset.filter(stamp_updated__gt=hour)
        elif pk =="6":
            queryset = queryset.filter(stamp_updated__gt=_6hours)
        elif pk== "24":
            queryset = queryset.filter(stamp_updated__gt=_24hours)
        queryset = queryset.annotate(traffic=Sum('bytes'))
        queryset = queryset.annotate(sum_packets=Sum('packets')).order_by('-sum_packets')[:10]
        return queryset

    def top_packets_out(self, pk): 
        queryset = self.values('ip_src')
        if pk== "1":
            queryset = queryset.filter(stamp_updated__gt=hour)
        elif pk== "6":
            queryset = queryset.filter(stamp_updated__gt=_6hours)
        elif pk =="24":
            queryset = queryset.filter(stamp_updated__gt=_24hours)
        queryset = queryset.annotate(traffic=Sum('bytes'))
        queryset = queryset.annotate(sum_packets=Sum('packets')).order_by('-sum_packets')[:10]       
        return queryset

    def top_app_in(self, pk):
        import socket
        queryset = self.values('dst_port')
        if pk== "1":
            queryset = queryset.filter(stamp_updated__gt=hour)
        elif pk== "6":
            queryset = queryset.filter(stamp_updated__gt=_6hours)
        elif pk =="24":
            queryset = queryset.filter(stamp_updated__gt=_24hours)
        queryset = queryset.annotate(traffic=Sum('bytes')).order_by('-traffic')[:10]
        for obj in queryset:
            try:
                if obj['dst_port']:
                    obj['dst_port'] = socket.getservbyport(obj['dst_port']) +' (port ' + str(obj['dst_port'])+')'
            except OSError:
                obj['dst_port'] = 'Unknown Application (port ' + str(obj['dst_port'])+')'
        return queryset

    def top_app_out(self, pk):
        import socket
        queryset = self.values('src_port')
        if pk =="1":
            queryset = queryset.filter(stamp_updated__gt=hour)
        elif pk =="6":
            queryset = queryset.filter(stamp_updated__gt=_6hours)
        elif pk== "24":
            queryset = queryset.filter(stamp_updated__gt=_24hours)
        queryset = queryset.annotate(traffic=Sum('bytes')).order_by('-traffic')[:10]
        for obj in queryset:
            try:
                if obj['src_port']:
                    obj['src_port'] = socket.getservbyport(obj['src_port']) +' (port ' + str(obj['src_port'])+')'
            except OSError:
                obj['src_port'] = 'Unknown Application (port ' + str(obj['src_port'])+')'
        return queryset       


class AcctIn1D(models.Model):
    id = models.BigIntegerField(primary_key=True)
    ip_dst = models.CharField(max_length=15)
    packets = models.IntegerField()
    bytes = models.BigIntegerField()
    stamp_inserted = models.DateTimeField()
    stamp_updated = models.DateTimeField(blank=True, null=True)
    
    objects = FlowQuerySets.as_manager()

    class Meta:
        managed = False
        db_table = 'acct_in_1d'


class AcctOut1D(models.Model):
    id = models.BigIntegerField(primary_key=True)
    ip_src = models.CharField(max_length=15)
    packets = models.IntegerField()
    bytes = models.BigIntegerField()
    stamp_inserted = models.DateTimeField()
    stamp_updated = models.DateTimeField(blank=True, null=True)
    
    objects = FlowQuerySets.as_manager()

    class Meta:
        managed = False
        db_table = 'acct_out_1d'

class AcctIn5M(models.Model):
    id = models.BigIntegerField(primary_key=True)
    ip_dst = models.CharField(max_length=15)
    dst_port = models.IntegerField()
    ip_proto = models.CharField(max_length=6)
    packets = models.IntegerField()
    bytes = models.BigIntegerField()
    stamp_inserted = models.DateTimeField()
    stamp_updated = models.DateTimeField(blank=True, null=True)
    
    objects = FlowQuerySets.as_manager()

    class Meta:
        managed = False
        db_table = 'acct_in_5m'


class AcctOut5M(models.Model):
    id = models.BigIntegerField(primary_key=True)
    ip_src = models.CharField(max_length=15)
    src_port = models.IntegerField()
    ip_proto = models.CharField(max_length=6)
    packets = models.IntegerField()
    bytes = models.BigIntegerField()
    stamp_inserted = models.DateTimeField()
    stamp_updated = models.DateTimeField(blank=True, null=True)
    
    objects = FlowQuerySets.as_manager()

    class Meta:
        managed = False
        db_table = 'acct_out_5m'

