# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-25 15:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('job', '0004_auto_20170119_1140'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('applicant', '0004_auto_20170124_1003'),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidacy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('M', 'Matching'), ('L', 'Like'), ('R', "Demande d'entretien"), ('V', 'Vidéo'), ('S', 'Retenu'), ('N', 'Non retenu')], max_length=1, verbose_name='status')),
                ('date_matching', models.DateTimeField(blank=True, null=True, verbose_name='date du matching')),
                ('date_like', models.DateTimeField(blank=True, null=True, verbose_name='date du like')),
                ('date_request', models.DateTimeField(blank=True, null=True, verbose_name='date de la demande')),
                ('date_video', models.DateTimeField(blank=True, null=True, verbose_name='date de la video')),
                ('date_decision', models.DateTimeField(blank=True, null=True, verbose_name='date de la décision')),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='applicant.Applicant', verbose_name='postulant')),
                ('collaborator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='collaborateur')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.Job', verbose_name='offre')),
            ],
            options={
                'verbose_name': 'Candidature',
                'verbose_name_plural': 'Candidatures',
            },
        ),
        migrations.CreateModel(
            name='CandidacyComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('message', models.TextField(verbose_name='commentaire')),
                ('candidacy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='candidacy.Candidacy', verbose_name='candidature')),
                ('collaborator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='collaborateur')),
            ],
            options={
                'verbose_name': 'commentaire',
                'verbose_name_plural': 'commentaires',
            },
        ),
    ]
