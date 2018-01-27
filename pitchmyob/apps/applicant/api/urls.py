# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from rest_framework.routers import SimpleRouter

from django.conf.urls import url

from .views import (ApplicantExperienceViewSet, ApplicantEducationViewSet, ApplicantSkillViewSet,
                    ApplicantLanguageViewSet, ApplicantInterestViewSet, ApplicantMeAPIView, ApplicantResumeAPIView)


router = SimpleRouter()
router.register('applicantexperiences', ApplicantExperienceViewSet, base_name='applicantexperience')
router.register('applicanteducations', ApplicantEducationViewSet, base_name='applicanteducation')
router.register('applicantskills', ApplicantSkillViewSet, base_name='applicantskill')
router.register('applicantlanguages', ApplicantLanguageViewSet, base_name='applicantlanguage')
router.register('applicantinterests', ApplicantInterestViewSet, base_name='applicantinterest')

urlpatterns = router.urls + [
    url(r'^applicant/resume/(?P<pk>\d+)', ApplicantResumeAPIView.as_view(), name='applicant-resmue'),
    url(r'^applicant/me', ApplicantMeAPIView.as_view(), name='applicant-me'),
]
