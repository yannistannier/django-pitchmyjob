# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ApplicantConfig(AppConfig):
    name = 'apps.applicant'
    verbose_name = _('Postulants')
