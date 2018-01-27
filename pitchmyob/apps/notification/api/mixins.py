# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.core.exceptions import ImproperlyConfigured

from ..utils import NotificationHandler


class NotificationtMixin(object):
    notification_type = None
    map_action_to_notification_type = None

    def get_notification_type(self):
        if not self.notification_type and not self.map_action_to_notification_type:
            raise ImproperlyConfigured('"%s" should include a `notification_type` or `map_action_to_notification_type`'
                                       'attribute.' % self.__class__.__name__)
        if self.notification_type:
            return self.notification_type
        else:
            return self.map_action_to_notification_type.get(self.action)

    def send_notification(self, instance, emitter):
        notification_type = self.get_notification_type()
        if notification_type:
            NotificationHandler(request=self.request, type_name=notification_type, emmiter=emitter,
                                action_object=instance).send()

    def perform_create(self, serializer):
        super(NotificationtMixin, self).perform_create(serializer)
        self.send_notification(serializer.instance, self.request.user)

    def perform_update(self, serializer):
        super(NotificationtMixin, self).perform_update(serializer)
        self.send_notification(serializer.instance, self.request.user)

    def perform_destroy(self, instance):
        self.send_notification(instance, self.request.user)
        super(NotificationtMixin, self).perform_destroy(instance)
