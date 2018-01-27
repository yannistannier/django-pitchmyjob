# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from model_utils.models import TimeStampedModel

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Candidacy(models.Model):
    MATCHING = 'M'
    LIKE = 'L'
    REQUEST = 'R'
    VIDEO = 'V'
    SELECTED = 'S'
    NOT_SELECTED = 'N'

    STATUS_CHOICES = (
        (MATCHING, _('Matching')),
        (LIKE, _('Like')),
        (REQUEST, _('Demande d\'entretien')),
        (VIDEO, _('Vidéo')),
        (SELECTED, _('Retenu')),
        (NOT_SELECTED, _('Non retenu')),
    )

    job = models.ForeignKey('job.Job', verbose_name=_('offre'))
    applicant = models.ForeignKey('applicant.Applicant', verbose_name=_('postulant'))
    collaborator = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, verbose_name=_('collaborateur'))
    status = models.CharField(_('status'), max_length=1, choices=STATUS_CHOICES)
    date_matching = models.DateTimeField(_('date du matching'), blank=True, null=True)
    date_like = models.DateTimeField(_('date du like'), blank=True, null=True)
    date_request = models.DateTimeField(_('date de la demande'), blank=True, null=True)
    date_video = models.DateTimeField(_('date de la video'), blank=True, null=True)
    date_decision = models.DateTimeField(_('date de la décision'), blank=True, null=True)
    matching_score = models.PositiveSmallIntegerField(_('score matching'), default=0)

    class Meta:
        verbose_name = _('Candidature')
        verbose_name_plural = _('Candidatures')
        unique_together = ('job', 'applicant')

    def __str__(self):
        return '{} - {}'.format(self.job, self.applicant)

    @property
    def is_matching(self):
        return self.status == self.MATCHING


@python_2_unicode_compatible
class CandidacyComment(TimeStampedModel, models.Model):
    candidacy = models.ForeignKey('candidacy.Candidacy', verbose_name=_('candidature'))
    collaborator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('collaborateur'))
    message = models.TextField(_('commentaire'))

    class Meta:
        verbose_name = _('commentaire')
        verbose_name_plural = _('commentaires')

    def __str__(self):
        return '{} - {}'.format(self.candidacy.pk, self.collaborator)
