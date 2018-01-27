# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from apps.core.behaviors import Localisation

from .behaviors import StartEndDate


@python_2_unicode_compatible
class Applicant(Localisation, models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_('utilisateur'))
    title = models.CharField(_('titre'), max_length=250, blank=True)
    birthday = models.DateField(_('date de naissance'), null=True, blank=True)
    description = models.TextField(_('description'), blank=True)
    url = models.CharField(_('lien'), max_length=250, blank=True)
    wanted_skills = ArrayField(models.CharField(_('skill'), max_length=250), null=True, blank=True,
                               verbose_name=_('compétences recherchées'))
    wanted_jobs = ArrayField(models.CharField(_('job'), max_length=250), null=True, blank=True,
                             verbose_name=_('postes recherchés'))
    wanted_contracts = models.ManyToManyField('data.ContractType', blank=True,
                                              verbose_name=_('types de contrat recherchés'))

    class Meta:
        verbose_name = _('postulant')
        verbose_name_plural = _('postulants')

    def __str__(self):
        return '{} - {}'.format(self.user, self.title)


@python_2_unicode_compatible
class ApplicantExperience(StartEndDate, models.Model):
    applicant = models.ForeignKey('applicant.Applicant', related_name='experiences', verbose_name=_('postulant'))
    company = models.CharField(_('raison sociale'), max_length=250)
    position = models.CharField(_('poste'), max_length=250)
    location = models.CharField(_('lieu'), max_length=250, blank=True)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        verbose_name = _('expérience')
        verbose_name_plural = _('expériences')
        ordering = ['-date_start', '-date_end']

    def __str__(self):
        return '{} - {}'.format(self.company, self.position)


@python_2_unicode_compatible
class ApplicantEducation(StartEndDate, models.Model):
    applicant = models.ForeignKey('applicant.Applicant', related_name='educations', verbose_name=_('postulant'))
    school = models.CharField(_('établissement'), max_length=250)
    degree = models.CharField(_('formation'), max_length=250)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        verbose_name = _('formation')
        verbose_name_plural = _('formations')
        ordering = ['-date_start', '-date_end']

    def __str__(self):
        return '{} - {}'.format(self.school, self.degree)


@python_2_unicode_compatible
class ApplicantSkill(models.Model):
    applicant = models.ForeignKey('applicant.Applicant', related_name='skills', verbose_name=_('postulant'))
    name = models.CharField(_('nom'), max_length=250)
    level = models.PositiveSmallIntegerField(_('niveau'), null=True, blank=True)

    class Meta:
        verbose_name = _('compétence')
        verbose_name_plural = _('compétences')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class ApplicantLanguage(models.Model):
    applicant = models.ForeignKey('applicant.Applicant', related_name='languages', verbose_name=_('postulant'))
    name = models.CharField(_('nom'), max_length=250)
    level = models.PositiveSmallIntegerField(_('niveau'), null=True, blank=True)

    class Meta:
        verbose_name = _('langue')
        verbose_name_plural = _('langues')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class ApplicantInterest(models.Model):
    applicant = models.ForeignKey('applicant.Applicant', related_name='interests', verbose_name=_('postulant'))
    name = models.CharField(_('nom'), max_length=250)

    class Meta:
        verbose_name = _('intérêt')
        verbose_name_plural = _('intérêts')

    def __str__(self):
        return self.name
