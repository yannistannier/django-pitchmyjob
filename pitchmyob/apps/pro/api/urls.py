# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from rest_framework.routers import SimpleRouter

from django.conf.urls import url

from .views import ProMeAPIView, ProCollaboratorViewSet


router = SimpleRouter()
router.register('pro/collaborators', ProCollaboratorViewSet)


urlpatterns = router.urls + [
    url(r'^pro/me', ProMeAPIView.as_view(), name="pro"),
]
