# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-19 16:54
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Applicant',
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
                ('title', models.CharField(blank=True, max_length=250, verbose_name='titre')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='date de naissance')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('url', models.CharField(blank=True, max_length=250, verbose_name='lien')),
                ('wanted_skills', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=250, verbose_name='skill'), size=None, verbose_name='compétences recherchées')),
                ('wanted_jobs', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=250, verbose_name='job'), size=None, verbose_name='postes recherchés')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='utilisateur')),
                ('wanted_contracts', models.ManyToManyField(blank=True, to='data.ContractType', verbose_name='types de contrat recherchés')),
            ],
            options={
                'verbose_name': 'postulant',
                'verbose_name_plural': 'postulants',
            },
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_start', models.DateField(blank=True, null=True, verbose_name='date de début')),
                ('date_end', models.DateField(blank=True, null=True, verbose_name='date de fin')),
                ('company', models.CharField(max_length=250, verbose_name='raison sociale')),
                ('position', models.CharField(max_length=250, verbose_name='poste')),
                ('location', models.CharField(blank=True, max_length=250, verbose_name='lieu')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='applicant.Applicant', verbose_name='postulant')),
            ],
            options={
                'verbose_name': 'expérience',
                'verbose_name_plural': 'expériences',
                'ordering': ['-date_start', '-date_end'],
            },
        ),
        migrations.CreateModel(
            name='Formation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_start', models.DateField(blank=True, null=True, verbose_name='date de début')),
                ('date_end', models.DateField(blank=True, null=True, verbose_name='date de fin')),
                ('school', models.CharField(max_length=250, verbose_name='établissement')),
                ('degree', models.CharField(max_length=250, verbose_name='formation')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='applicant.Applicant', verbose_name='postulant')),
            ],
            options={
                'verbose_name': 'formation',
                'verbose_name_plural': 'formations',
                'ordering': ['-date_start', '-date_end'],
            },
        ),
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='nom')),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='applicant.Applicant', verbose_name='postulant')),
            ],
            options={
                'verbose_name': 'intérêt',
                'verbose_name_plural': 'intérêts',
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='nom')),
                ('level', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='niveau')),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='applicant.Applicant', verbose_name='postulant')),
            ],
            options={
                'verbose_name': 'langue',
                'verbose_name_plural': 'langues',
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='nom')),
                ('level', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='niveau')),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='applicant.Applicant', verbose_name='postulant')),
            ],
            options={
                'verbose_name': 'compétence',
                'verbose_name_plural': 'compétences',
            },
        ),
    ]