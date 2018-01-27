# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from apps.core.behaviors import Localisation
from apps.core.fields import ImageField


@python_2_unicode_compatible
class Pro(Localisation, models.Model):
    DEFAULT_LOGO = 'pro/logo/default.jpg'

    company = models.CharField(_('raison sociale'), max_length=250)
    website = models.CharField(_('site web'), max_length=250, blank=True)
    description = models.TextField(_('description'), blank=True)
    phone = models.CharField(_('phone'), max_length=250, blank=True)
    industry = models.ForeignKey('data.Industry', default=1, verbose_name=_('secteur d\'activité'))
    employes = models.ForeignKey('data.Employee', null=True, verbose_name=_('nombre d\'employés'))
    ca = models.CharField(_('chiffre d\'affaire'), max_length=250, blank=True)
    logo = ImageField(_('logo'), blank=True, default=DEFAULT_LOGO)
    is_active = models.BooleanField(_('est actif'), default=True)

    class Meta:
        verbose_name = _('pro')
        verbose_name_plural = _('pros')

    def __str__(self):
        return self.company
