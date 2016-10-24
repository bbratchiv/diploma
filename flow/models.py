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
from django.core import validators




hour = datetime.now() - timedelta(hours=1)
_6hours = datetime.now() - timedelta(hours=6)
_24hours = datetime.now() - timedelta(hours=24)

class FlowQuerySets(models.QuerySet):

    
    def top_ip_in(self, pk, device):
        queryset = self.values('ip_dst', 'ip_proto').filter(peer_ip_src=device)
        if pk =="0":
            pass
        elif pk == "1":
            queryset = queryset.filter(stamp_updated__gt= hour)
        elif pk ==  "6":
            queryset = queryset.filter(stamp_updated__gt=_6hours)
        elif pk == "24":
            queryset = queryset.filter(stamp_updated__gt=_24hours)

        queryset = queryset.annotate(traffic=Sum('bytes')).order_by('-traffic')[:10]
        return queryset

    def top_ip_out(self, pk, device):
        queryset = self.values('ip_src', 'ip_proto').filter(peer_ip_src=device)
        if pk =="0":
            pass
        elif pk == "1":
            queryset = queryset.filter(stamp_updated__gt=hour)
        elif pk == "6":
            queryset = queryset.filter(stamp_updated__gt=_6hours)
        elif pk =="24":
            queryset = queryset.filter(stamp_updated__gt=_24hours)
        queryset = queryset.annotate(traffic=Sum('bytes')).order_by('-traffic')[:10]
        return queryset

    def top_proto_in(self, pk, device): 
        queryset = self.values('ip_proto').filter(peer_ip_src=device)
        if pk =="0":
            pass
        elif pk == "1":
            queryset = queryset.filter(stamp_updated__gt=hour)
        elif pk == "6":
            queryset = queryset.filter(stamp_updated__gt=_6hours)
        elif pk == "24":
            queryset = queryset.filter(stamp_updated__gt=_24hours)
        queryset = queryset.annotate(traffic=Sum('bytes')).order_by('-traffic')[:10]
        return queryset

    def top_proto_out(self, pk, device): 
        queryset = self.values('ip_proto').filter(peer_ip_src=device)
        if pk =="0":
            pass
        elif pk == "1":
            queryset = queryset.filter(stamp_updated__gt=hour)
        elif pk == "6":
            queryset = queryset.filter(stamp_updated__gt=_6hours)
        elif pk == "24":
            queryset = queryset.filter(stamp_updated__gt=_24hours)
        queryset = queryset.annotate(traffic=Sum('bytes')).order_by('-traffic')[:10]
        return queryset
    
    def top_packets_in(self, pk, device): 
        queryset = self.values('ip_dst').filter(peer_ip_src=device)
        if pk =="0":
            pass
        elif pk =="1":
            queryset = queryset.filter(stamp_updated__gt=hour)
        elif pk =="6":
            queryset = queryset.filter(stamp_updated__gt=_6hours)
        elif pk== "24":
            queryset = queryset.filter(stamp_updated__gt=_24hours)
        queryset = queryset.annotate(traffic=Sum('bytes'))
        queryset = queryset.annotate(sum_packets=Sum('packets')).order_by('-sum_packets')[:10]
        return queryset

    def top_packets_out(self, pk, device): 
        queryset = self.values('ip_src').filter(peer_ip_src=device)
        if pk =="0":
            pass
        elif pk== "1":
            queryset = queryset.filter(stamp_updated__gt=hour)
        elif pk== "6":
            queryset = queryset.filter(stamp_updated__gt=_6hours)
        elif pk =="24":
            queryset = queryset.filter(stamp_updated__gt=_24hours)
        queryset = queryset.annotate(traffic=Sum('bytes'))
        queryset = queryset.annotate(sum_packets=Sum('packets')).order_by('-sum_packets')[:10]       
        return queryset

    def top_app_in(self, pk, device):
        import socket
        queryset = self.values('dst_port').filter(peer_ip_src=device)
        if pk =="0":
            pass
        elif pk== "1":
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
                obj['dst_port'] = 'port ' + str(obj['dst_port'])
        return queryset

    def top_app_out(self, pk, device):
        import socket
        queryset = self.values('src_port').filter(peer_ip_src=device)
        if pk =="0":
            pass
        elif pk =="1":
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
                obj['src_port'] = 'port ' + str(obj['src_port'])
        return queryset       


    def traffic(self,device):
        return self.values('stamp_updated').filter(peer_ip_src=device)\
                                        .annotate(traffic=Sum('bytes'))
#    def traffic(self, device):
#        return self.values('stamp_updated', 'bytes').order_by('-stamp_updated')

class TrafficIn(models.Model):
    id = models.BigIntegerField(primary_key=True)
    ip_dst = models.CharField(max_length=15)
    dst_port = models.IntegerField()
    ip_proto = models.CharField(max_length=6)
    packets = models.IntegerField()
    bytes = models.BigIntegerField()
    peer_ip_src = models.CharField(max_length=15) #device ip
    stamp_inserted = models.DateTimeField()
    stamp_updated = models.DateTimeField(blank=True, null=True)
    
    objects = FlowQuerySets.as_manager()

    class Meta:
        managed = False
        db_table = 'traffic_in'


class TrafficOut(models.Model):
    id = models.BigIntegerField(primary_key=True)
    ip_src = models.CharField(max_length=15)
    src_port = models.IntegerField()
    ip_proto = models.CharField(max_length=6)
    packets = models.IntegerField()
    bytes = models.BigIntegerField()
    peer_ip_src = models.CharField(max_length=15) #device ip
    stamp_inserted = models.DateTimeField()
    stamp_updated = models.DateTimeField(blank=True, null=True)
    objects = FlowQuerySets.as_manager()

    class Meta:
        managed = False
        db_table = 'traffic_out'


class Billing(models.Model):
    billing_id = models.SmallIntegerField(primary_key= True)
    rate_name = models.CharField(max_length=15)
    billable = models.BooleanField(default = False)
    cost_rate = models.FloatField(max_length=10)

    class Meta:
        managed = True
        db_table = 'billing'


class Devices(models.Model):
    device_id = models.SmallIntegerField(primary_key=True)
    device_name = models.CharField(max_length=20)
    device_ip = models.CharField(max_length=15)
    billing = models.ForeignKey(Billing, on_delete=models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'devices'

