# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-18 12:40
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pro', '0001_initial'),
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=250, verbose_name='adresse')),
                ('latitude', models.FloatField(blank=True, null=True, verbose_name='latitude')),
                ('longitude', models.FloatField(blank=True, null=True, verbose_name='longitude')),
                ('street_number', models.CharField(blank=True, max_length=250, verbose_name='numéro de rue')),
                ('route', models.CharField(blank=True, max_length=250, verbose_name='nom de rue')),
                ('cp', models.CharField(blank=True, max_length=250, verbose_name='code postal')),
                ('locality', models.CharField(blank=True, max_length=250, verbose_name='ville')),
                ('administrative_area_level_1', models.CharField(blank=True, max_length=250, verbose_name='région')),
                ('administrative_area_level_2', models.CharField(blank=True, max_length=250, verbose_name='département')),
                ('country', models.CharField(blank=True, max_length=250, verbose_name='pays')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(max_length=250, verbose_name="titre de l'offre")),
                ('salary', models.CharField(max_length=250, verbose_name='salaire')),
                ('skills', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=250, verbose_name='skill'), size=None, verbose_name='compétences recherchées')),
                ('description', models.TextField(verbose_name='description')),
                ('view_counter', models.PositiveIntegerField(default=0, verbose_name='nombre de vue')),
                ('last_payment', models.DateTimeField(blank=True, null=True, verbose_name='dernier paiement')),
                ('is_complete', models.BooleanField(default=False, verbose_name='est complet')),
                ('is_active', models.BooleanField(default=False, verbose_name='est actif')),
                ('contract_types', models.ManyToManyField(to='data.ContractType', verbose_name='types de contrat')),
                ('experiences', models.ManyToManyField(to='data.Experience', verbose_name='expériences')),
                ('pro', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pro.Pro', verbose_name='pro')),
                ('study_levels', models.ManyToManyField(to='data.StudyLevel', verbose_name="niveaux d'étude")),
            ],
            options={
                'verbose_name': 'offre',
                'verbose_name_plural': 'offres',
            },
        ),
        migrations.CreateModel(
            name='JobQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=250)),
                ('order', models.PositiveSmallIntegerField(default=1, verbose_name='ordre')),
                ('job', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='job.Job')),
            ],
            options={
                'verbose_name': 'question',
                'verbose_name_plural': 'questions',
                'ordering': ['order'],
            },
        ),
    ]
