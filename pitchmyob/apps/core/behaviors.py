# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Localisation(models.Model):
    address = models.CharField(_('adresse'), max_length=250, blank=True)
    latitude = models.FloatField(_('latitude'), blank=True, null=True)
    longitude = models.FloatField(_('longitude'), blank=True, null=True)
    street_number = models.CharField(_('numéro de rue'), max_length=250, blank=True)
    route = models.CharField(_('nom de rue'), max_length=250, blank=True)
    cp = models.CharField(_('code postal'), max_length=250, blank=True)
    locality = models.CharField(_('ville'), max_length=250, blank=True)
    administrative_area_level_1 = models.CharField(_('région'), max_length=250, blank=True)
    administrative_area_level_2 = models.CharField(_('département'), max_length=250, blank=True)
    country = models.CharField(_('pays'), max_length=250, blank=True)

    class Meta:
        abstract = True
