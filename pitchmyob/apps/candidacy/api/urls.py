# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from rest_framework.routers import SimpleRouter

from django.conf.urls import url

from .views import (CandidacyProListAPIView, CandidacyProRetrieveAPIView, CandidacyProRequestAPIView,
                    CandidacyProApproveAPIView, CandidacyProDisapproveAPIView, CandidacyApplicantListAPIView,
                    CandidacyApplicantRetrieveAPIView, CandidacyApplicantLikeAPIView,
                    CandidacyApplicantPostulateAPIView, CandidacyProCommentViewSet, CandidacyProExistsAPIView)


router = SimpleRouter()
router.register(r'^pro/candidacy/comments', CandidacyProCommentViewSet, base_name='procandidacy-comment')

urlpatterns = router.urls + [
    url(r'^pro/candidacies/(?P<job_pk>\d+)', CandidacyProListAPIView.as_view(), name='procandidacy-list'),
    url(r'^pro/candidacy/(?P<pk>\d+)/approve', CandidacyProApproveAPIView.as_view(), name='procandidacy-approve'),
    url(r'^pro/candidacy/(?P<pk>\d+)/disapprove', CandidacyProDisapproveAPIView.as_view(),
        name='procandidacy-disapprove'),
    url(r'^pro/candidacy/(?P<pk>\d+)', CandidacyProRetrieveAPIView.as_view(), name='procandidacy-detail'),
    url(r'^pro/candidacy/request', CandidacyProRequestAPIView.as_view(), name='procandidacy-request'),
    url(r'^pro/candidacy/exists', CandidacyProExistsAPIView.as_view(), name='procandidacy-exists'),
    url(r'^applicant/candidacies', CandidacyApplicantListAPIView.as_view(), name='applicantcandidacy-list'),
    url(r'^applicant/candidacy/(?P<pk>\d+)/like', CandidacyApplicantLikeAPIView.as_view(),
        name='applicantcandidacy-like'),
    url(r'^applicant/candidacy/(?P<pk>\d+)/postulate', CandidacyApplicantPostulateAPIView.as_view(),
        name='applicantcandidacy-postulate'),
    url(r'^applicant/candidacy/(?P<pk>\d+)', CandidacyApplicantRetrieveAPIView.as_view(),
        name='applicantcandidacy-detail'),
]
