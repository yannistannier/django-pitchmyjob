# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-26 12:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0004_auto_20170119_1140'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='request_credits',
            field=models.PositiveIntegerField(default=0, verbose_name="crédits demande d'entretien"),
        ),
    ]