# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.utils.translation import ugettext_lazy as _

from .behaviors import DataModel


class Industry(DataModel):
    class Meta(DataModel.Meta):
        verbose_name = _('Secteur d\'activité')
        verbose_name_plural = _('Secteurs d\'activité')


class Employee(DataModel):
    class Meta(DataModel.Meta):
        verbose_name = _('Nombre d\'employés')
        verbose_name_plural = _('Nombre d\'employés')


class ContractType(DataModel):
    class Meta(DataModel.Meta):
        verbose_name = _('Type de contrat')
        verbose_name_plural = _('Types de contrat')


class Experience(DataModel):
    class Meta(DataModel.Meta):
        verbose_name = _('Expérience')
        verbose_name_plural = _('Expérience')


class StudyLevel(DataModel):
    class Meta(DataModel.Meta):
        verbose_name = _('Niveau d\'étude')
        verbose_name_plural = _('Niveaux d\'étude')
