# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-18 17:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0002_remove_job_is_complete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='est actif'),
        ),
    ]
