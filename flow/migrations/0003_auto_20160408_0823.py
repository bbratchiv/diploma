# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-08 08:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flow', '0002_devices'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devices',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]