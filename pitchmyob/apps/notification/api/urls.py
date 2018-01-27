# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from rest_framework.routers import SimpleRouter

from .views import NotificationViewSet


router = SimpleRouter()
router.register('notifications', NotificationViewSet, base_name='notification')

urlpatterns = router.urls
