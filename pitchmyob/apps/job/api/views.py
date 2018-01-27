# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import boto3
import json

from rest_framework import decorators, permissions, status, generics
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from django.db.models import Count
from django.conf import settings
from django.shortcuts import get_object_or_404

from apps.candidacy.models import Candidacy
from apps.core.api.mixins import IsActiveDestroyMixin
from apps.core.utils import Email
from apps.notification import types
from apps.notification.api.mixins import NotificationtMixin
from apps.pro.api.permissions import IsProUser
from apps.event.mixins import EventJobViewSetMixin
from apps.authentication.models import User

from ..models import Job, JobQuestion, InvitationEmail
from .filters import JobFilter
from .pagination import JobPagination
from .serializers import JobSerializer, JobQuestionSerializer, JobPublishSerializer, JobMatchingSerialier, InvitationEmailSerializer, CheckInvitationEmail


class JobViewSet(EventJobViewSetMixin, NotificationtMixin, IsActiveDestroyMixin, ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsProUser]
    serializer_class = JobSerializer
    pagination_class = JobPagination
    map_action_to_notification_type = {
        'create': types.PRO_JOB_ADDED,
        'update': types.PRO_JOB_UPDATED,
        'destroy': types.PRO_JOB_DELETED,
    }
    filter_class = JobFilter
    search_fields = ('title', 'description')

    def get_serializer_context(self):
        context = super(JobViewSet, self).get_serializer_context()

        not_matching = Candidacy.objects.filter(job__pro=self.request.user.pro).exclude(status=Candidacy.MATCHING)
        candidacies_count = Job.objects.filter(candidacy__in=not_matching).annotate(Count('candidacy')) \
                                       .values('id', 'candidacy__count')
        context['candidacies_count'] = {job['id']: job['candidacy__count'] for job in candidacies_count}
        return context

    def get_queryset(self):
        qs = Job.objects.prefetch_related('contract_types', 'experiences', 'study_levels')
        return qs.filter(pro=self.request.user.pro, is_active=True)

    @decorators.list_route(methods=['put', 'patch'], serializer_class=JobPublishSerializer,
                           notification_type=types.PRO_JOB_PUBLISHED)
    def publish(self, request, pk=None):
        self.kwargs['pk'] = request.data.get('job', None)
        return self.update(request)

    @decorators.list_route(methods=['get'])
    def count(self, request, pk=None):
        return Response({
            'pending': Job.objects.filter(pro=request.user.pro, is_active=True).is_pending().count(),
            'visible': Job.objects.filter(pro=request.user.pro, is_active=True).is_visible().count(),
            'expired': Job.objects.filter(pro=request.user.pro, is_active=True).is_expired().count(),
        })

    @decorators.detail_route(methods=['get'], url_path='count-candidacies')
    def count_candidacies(self, request, pk=None):
        return Response({
            'like': Candidacy.objects.filter(job__pro=request.user.pro, job_id=pk, job__is_active=True,
                                             status=Candidacy.LIKE).count(),
            'request': Candidacy.objects.filter(job__pro=request.user.pro, job_id=pk, job__is_active=True,
                                                status=Candidacy.REQUEST).count(),
            'video': Candidacy.objects.filter(job__pro=request.user.pro, job_id=pk, job__is_active=True,
                                              status=Candidacy.VIDEO).count(),
            'selected': Candidacy.objects.filter(job__pro=request.user.pro, job_id=pk, job__is_active=True,
                                                 status=Candidacy.SELECTED).count(),
            'not_selected': Candidacy.objects.filter(job__pro=request.user.pro, job_id=pk, job__is_active=True,
                                                     status=Candidacy.NOT_SELECTED).count(),
        })

    @decorators.list_route(methods=['post'])
    def matching(self, request, pk=None):
        serializer = JobMatchingSerialier(data=request.data)
        serializer.is_valid(raise_exception=True)

        if Job.objects.filter(pro=request.user.pro, pk=serializer.data.get('job')).is_visible().exists():
            lm = boto3.client("lambda")
            response = lm.invoke(
                FunctionName=settings.MATCHING_LAMBDA,
                InvocationType='RequestResponse',
                Payload=json.dumps(serializer.data)
            )
            results = response['Payload'].read().decode()

            return Response(json.loads(results))

        return Response(status=status.HTTP_401_UNAUTHORIZED)


    @decorators.detail_route(methods=['get', 'post'])
    def invitation(self, request, pk):
        if Job.objects.filter(pk=pk, pro=request.user.pro).exists():
            if request.method == "POST":
                serializer = CheckInvitationEmail(data=request.data)
                serializer.is_valid(raise_exception=True)

                for email in serializer.data.get('emails'):
                    inv, inv_created = InvitationEmail.objects.get_or_create(job_id=pk, email=email)
                    if User.objects.filter(email=email).exists():
                        user = User.objects.get(email=email)
                        if user.is_applicant:
                            obj, created = Candidacy.objects.update_or_create(
                                job_id=pk,
                                applicant=user.applicant,
                                defaults={'status' : "R"}
                            )
                    else:
                        if inv_created:
                            context = {'email': email}
                            Email(subject='Invitation à passer entretien', to=email, context=context,
                                  template='applicant/requested.html').send()


            serializer = InvitationEmailSerializer(InvitationEmail.objects.filter(job=pk), many=True)
            return Response(serializer.data)

        return Response(status=status.HTTP_401_UNAUTHORIZED)


class JobQuestionViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsProUser]
    serializer_class = JobQuestionSerializer
    filter_fields = ('job',)

    def get_queryset(self):
        return JobQuestion.objects.filter(job__pro=self.request.user.pro, job__is_active=True)
