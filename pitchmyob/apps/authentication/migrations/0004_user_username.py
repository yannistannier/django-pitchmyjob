# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-20 10:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_remove_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=250, verbose_name='username'),
        ),
    ]