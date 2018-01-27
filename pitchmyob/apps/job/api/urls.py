# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from rest_framework.routers import SimpleRouter
from django.conf.urls import url

from .views import JobViewSet, JobQuestionViewSet


router = SimpleRouter()
router.register('jobs', JobViewSet, base_name='job')
router.register('jobquestions', JobQuestionViewSet, base_name='jobquestion')

urlpatterns = router.urls