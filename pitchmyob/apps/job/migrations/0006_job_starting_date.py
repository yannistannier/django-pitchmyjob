# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-20 12:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0005_job_request_credits'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='starting_date',
            field=models.CharField(default='', max_length=250, verbose_name="titre de l'offre"),
            preserve_default=False,
        ),
    ]
