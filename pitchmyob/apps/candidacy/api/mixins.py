# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from rest_framework import permissions

from django.db.models import Q

from apps.applicant.api.permissions import IsApplicantUser
from apps.pro.api.permissions import IsProUser

from .serializers import (CandidacyProReadSerializer, CandidacyProRequestSerializer, CandidacyProApproveSerializer,
                          CandidacyProDisapproveSerializer, CandidacyApplicantReadSerializer,
                          CandidacyApplicantLikeSerializer, CandidacyApplicantVideoSerializer,
                          CandidacyProResumeSerializer)
from ..models import Candidacy


class CandidacyMixin(object):
    def get_serializer_class(self):
        url_name = self.request.resolver_match.url_name
        return self.serializers_class.get(url_name)


class CandidacyProPermissionMixin(object):
    permission_classes = [permissions.IsAuthenticated, IsProUser]


class CandidacyProMixin(CandidacyProPermissionMixin, CandidacyMixin):
    serializers_class = {
        'procandidacy-list': CandidacyProReadSerializer,
        'procandidacy-detail': CandidacyProReadSerializer,
        'procandidacy-request': CandidacyProRequestSerializer,
        'procandidacy-exists': CandidacyProResumeSerializer,
        'procandidacy-approve': CandidacyProApproveSerializer,
        'procandidacy-disapprove': CandidacyProDisapproveSerializer,
    }

    def get_queryset(self):
        qs_filter = {}
        if 'job_pk' in self.kwargs:
            qs_filter = {'job': self.kwargs.get('job_pk')}
        return Candidacy.objects.filter(~Q(status=Candidacy.MATCHING), job__pro=self.request.user.pro, **qs_filter)


class CandidacyApplicantMixin(CandidacyMixin):
    permission_classes = [permissions.IsAuthenticated, IsApplicantUser]
    serializers_class = {
        'applicantcandidacy-list': CandidacyApplicantReadSerializer,
        'applicantcandidacy-detail': CandidacyApplicantReadSerializer,
        'applicantcandidacy-like': CandidacyApplicantLikeSerializer,
        'applicantcandidacy-postulate': CandidacyApplicantVideoSerializer,
    }

    def get_queryset(self):
        return Candidacy.objects.filter(applicant=self.request.user.applicant)
