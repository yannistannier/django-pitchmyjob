# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-18 17:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='is_complete',
        ),
    ]
