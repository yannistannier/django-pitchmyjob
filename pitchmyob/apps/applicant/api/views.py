# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from rest_framework import generics, permissions
from rest_framework.viewsets import ModelViewSet

from apps.core.api.mixins import IsAuthenticatedMixin
from apps.event.mixins import EventApplicantViewSetMixin
from apps.pro.api.permissions import IsProUser

from .permissions import IsApplicantUser
from .serializers import (ApplicantMeSerializer, ApplicantExperienceSerializer, ApplicantEducationSerializer,
                          ApplicantSkillSerializer, ApplicantLanguageSerializer, ApplicantInterestSerializer,
                          ApplicantFullSerializer)
from ..models import (Applicant, ApplicantExperience, ApplicantEducation, ApplicantSkill, ApplicantLanguage,
                      ApplicantInterest)


class ApplicantMeAPIView(EventApplicantViewSetMixin, generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsApplicantUser]
    serializer_class = ApplicantMeSerializer
    event_type = 'applicant'

    def get_object(self):
        return self.request.user.applicant


class ApplicantResumeAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, IsProUser]
    serializer_class = ApplicantFullSerializer
    queryset = Applicant.objects.all()


class ApplicantExperienceViewSet(EventApplicantViewSetMixin, IsAuthenticatedMixin, ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsApplicantUser]
    serializer_class = ApplicantExperienceSerializer
    event_type = 'experience'

    def get_queryset(self):
        return ApplicantExperience.objects.filter(applicant__user=self.request.user)


class ApplicantEducationViewSet(EventApplicantViewSetMixin, IsAuthenticatedMixin, ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsApplicantUser]
    serializer_class = ApplicantEducationSerializer
    event_type = 'education'

    def get_queryset(self):
        return ApplicantEducation.objects.filter(applicant__user=self.request.user)


class ApplicantSkillViewSet(EventApplicantViewSetMixin, IsAuthenticatedMixin, ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsApplicantUser]
    serializer_class = ApplicantSkillSerializer
    event_type = 'skill'

    def get_queryset(self):
        return ApplicantSkill.objects.filter(applicant__user=self.request.user)


class ApplicantLanguageViewSet(EventApplicantViewSetMixin, IsAuthenticatedMixin, ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsApplicantUser]
    serializer_class = ApplicantLanguageSerializer
    event_type = 'language'

    def get_queryset(self):
        return ApplicantLanguage.objects.filter(applicant__user=self.request.user)


class ApplicantInterestViewSet(EventApplicantViewSetMixin, IsAuthenticatedMixin, ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsApplicantUser]
    serializer_class = ApplicantInterestSerializer
    event_type = 'interest'

    def get_queryset(self):
        return ApplicantInterest.objects.filter(applicant__user=self.request.user)
