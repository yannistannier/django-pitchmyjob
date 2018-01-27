# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class CandidacyMessage(models.Model):
    candidacy = models.ForeignKey('candidacy.Candidacy', verbose_name=_('candidature'))
    emmiter = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('émmeteur'))
    message = models.TextField(_('message'))
    created = models.DateTimeField(_('date de création'), auto_now_add=True)

    class Meta:
        verbose_name = _('message')
        verbose_name_plural = _('messages')

    def __str__(self):
        return '{} - {}'.format(candidacy, emmiter)


@python_2_unicode_compatible
class CandidacyMessageRead(models.Model):
    candidacy = models.ForeignKey('candidacy.Candidacy', verbose_name=_('candidature'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('utilisateur'))
    is_read = models.BooleanField(_('est lu'), default=False)
    date = models.DateTimeField(_('date de dernière lecture'), blank=True, null=True)

    class Meta:
        verbose_name = _('message lu')
        verbose_name_plural = _('messages lu')
        unique_together = ('candidacy', 'user')

    def __str__(self):
        return '{} - {}'.format(candidacy, user)
