# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Notification(models.Model):
    type_name = models.CharField(_('type de la notification'), max_length=250)
    emmiter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notification_sent',
                                verbose_name=_('émmeteur'))
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notification_received',
                                 verbose_name=_('receveur'))
    action_object_content_type = models.ForeignKey(ContentType, verbose_name=_('type de l\'objet lié'))
    action_object_id = models.PositiveIntegerField(_('identifiant de l\'objet lié'))
    action_object = GenericForeignKey('action_object_content_type', 'action_object_id')
    created = models.DateTimeField(_('date de création'), auto_now=True)
    is_unread = models.BooleanField(_('est non lu'), default=True)

    class Meta:
        verbose_name = _('notification')
        verbose_name_plural = _('notifications')
        ordering = ['-created']

    def __str__(self):
        return '{} > {} : {}'.format(self.emmiter.pk, self.receiver.pk, self.type_name)
