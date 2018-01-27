# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.db import models
from django.utils.translation import ugettext_lazy as _


class StartEndDate(models.Model):
    date_start = models.DateField(_('date de début'), null=True, blank=True)
    date_end = models.DateField(_('date de fin'), null=True, blank=True)

    class Meta:
        abstract = True
