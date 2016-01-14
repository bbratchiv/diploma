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


class Flow(models.Model):
    id = models.BigIntegerField(primary_key = True)
    ip_src = models.CharField(max_length=15)
    ip_dst = models.CharField(max_length=15)
    src_port = models.IntegerField()
    dst_port = models.IntegerField()
    ip_proto = models.CharField(max_length=6)
    packets = models.IntegerField()
    bytes = models.BigIntegerField()
    stamp_inserted = models.DateTimeField()
    stamp_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acct'
