# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from rest_framework.routers import SimpleRouter

from django.conf.urls import url

from .views import (CandidacyMessageViewSet, CandidacyMessageJobListAPIView, CandidacyMessageUnreadCountAPIView,
                    CandidacyMessageNotificationAPIView)


router = SimpleRouter()
router.register('messages', CandidacyMessageViewSet, base_name='message')

urlpatterns = [
    url(r'^messages/notification/', CandidacyMessageNotificationAPIView.as_view(), name='message-notification'),
    url(r'^messages/job/(?P<pk>\d+)', CandidacyMessageJobListAPIView.as_view(), name='message-job-list'),
    url(r'^messages/unread/count/', CandidacyMessageUnreadCountAPIView.as_view(), name='message-unread-count'),
] + router.urls
