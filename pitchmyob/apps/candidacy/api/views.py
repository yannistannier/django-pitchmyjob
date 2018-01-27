# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from rest_framework import generics, status, mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from django.db.models import F
from django.shortcuts import get_object_or_404

from apps.job.models import Job
from apps.notification import types
from apps.notification.api.mixins import NotificationtMixin

from .mixins import CandidacyProMixin, CandidacyApplicantMixin, CandidacyProPermissionMixin
from .pagination import CandidacyListPagination, CandidacyCommentsPagination
from .serializers import CandidacyProCommentSerializer
from ..models import Candidacy, CandidacyComment


class CandidacyProListAPIView(CandidacyProMixin, generics.ListAPIView):
    filter_fields = ('status',)
    search_fields = ('applicant__title', 'applicant__description',
                     'applicant__user__first_name', 'applicant__user__last_name', 'applicant__user__email')
    pagination_class = CandidacyListPagination


class CandidacyProRetrieveAPIView(CandidacyProMixin, generics.RetrieveAPIView):
    pass


class CandidacyProRequestAPIView(NotificationtMixin, CandidacyProMixin, generics.GenericAPIView):
    notification_type = types.APPLICANT_CANDIDACY_REQUESTED

    def post(self, request):
        job = request.data.get('job')
        applicant = request.data.get('applicant')

        candidacy = Candidacy.objects.filter(job=job, applicant=applicant).first()
        if candidacy:
            serializer = self.get_serializer(candidacy, data=request.data)
            serializer.is_valid(raise_exception=True)
            if candidacy.is_matching:
                Job.objects.filter(pk=job).update(request_credits=F('request_credits') - 1)
            serializer.save()
            self.send_notification(serializer.instance, request.user)
            return Response(serializer.data)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            self.send_notification(serializer.instance, request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class CandidacyProExistsAPIView(CandidacyProMixin, generics.GenericAPIView):
    def post(self, request):
        job = request.data.get('job')
        applicant = request.data.get('applicant')

        candidacy = get_object_or_404(Candidacy.objects.filter(job=job, applicant=applicant))
        serializer = self.get_serializer(candidacy)
        return Response(serializer.data)


class CandidacyProApproveAPIView(NotificationtMixin, CandidacyProMixin, generics.UpdateAPIView):
    notification_type = types.APPLICANT_CANDIDACY_APPROVED


class CandidacyProDisapproveAPIView(NotificationtMixin, CandidacyProMixin, generics.UpdateAPIView):
    notification_type = types.APPLICANT_CANDIDACY_DISAPPROVED


class CandidacyApplicantListAPIView(CandidacyApplicantMixin, generics.ListAPIView):
    filter_fields = ('status',)


class CandidacyApplicantRetrieveAPIView(CandidacyApplicantMixin, generics.RetrieveAPIView):
    pass


class CandidacyApplicantLikeAPIView(NotificationtMixin, CandidacyApplicantMixin, generics.UpdateAPIView):
    notification_type = types.PRO_JOB_LIKED


class CandidacyApplicantPostulateAPIView(NotificationtMixin, CandidacyApplicantMixin, generics.UpdateAPIView):
    notification_type = types.PRO_JOB_NEW_CANDIDACY


class CandidacyProCommentViewSet(NotificationtMixin,
                                 CandidacyProPermissionMixin,
                                 mixins.ListModelMixin,
                                 mixins.CreateModelMixin,
                                 mixins.DestroyModelMixin,
                                 GenericViewSet):
    notification_type = types.PRO_CANDIDACY_NEW_COMMENT
    pagination_class = CandidacyCommentsPagination
    serializer_class = CandidacyProCommentSerializer
    filter_fields = ('candidacy',)

    def get_queryset(self):
        return CandidacyComment.objects.filter(candidacy__job__pro=self.request.user.pro).order_by('-created')
