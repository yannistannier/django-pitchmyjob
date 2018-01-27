# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from rest_framework import permissions
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from django.db.models import Q
from django.utils import timezone

from apps.candidacy.models import Candidacy
from apps.notification import types
from apps.notification.api.mixins import NotificationtMixin
from apps.pro.api.permissions import IsProUser

from ..models import CandidacyMessage, CandidacyMessageRead
from .pagination import (CandidacyJobMessagePagination, CandidacyMessagesPagination,
                         CandidacyMessagesNotificationPagination)
from .serializers import CandidacyMessageSerializer, CandidacyMessageJobListSerializer


class CandidacyMessageViewSet(NotificationtMixin, ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CandidacyMessageSerializer
    filter_fields = ('candidacy',)
    pagination_class = CandidacyMessagesPagination
    notification_type = types.NEW_MESSAGE

    def get_queryset(self):
        qs_filter = {}
        if self.request.user.is_pro:
            qs_filter = {'candidacy__job__pro': self.request.user.pro}
        elif self.request.user.is_applicant:
            qs_filter = {'candidacy__applicant': self.request.user.applicant}
        queryset = CandidacyMessage.objects.filter(~Q(candidacy__status=Candidacy.MATCHING), **qs_filter)
        return queryset.order_by('-created')

    def list(self, request, *args, **kwargs):
        response = super(CandidacyMessageViewSet, self).list(request, *args, **kwargs)
        candidacy_id = self.request.GET.get('candidacy')
        if candidacy_id:
            qs_filter = {'user': self.request.user, 'candidacy_id': candidacy_id}
            candidacy_messsage_read, created = CandidacyMessageRead.objects.get_or_create(**qs_filter)
            candidacy_messsage_read.is_read = True
            candidacy_messsage_read.date = timezone.now()
            candidacy_messsage_read.save()
        return response


class CandidacyMessageJobListAPIView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsProUser]
    serializer_class = CandidacyMessageJobListSerializer
    pagination_class = CandidacyJobMessagePagination
    search_fields = ('candidacy__applicant__title', 'candidacy__applicant__description',
                     'candidacy__applicant__user__first_name', 'candidacy__applicant__user__last_name',
                     'candidacy__applicant__user__email')

    def get_queryset(self):
        qs_filter = {
            'candidacy__job': self.kwargs.get('pk'),
            'candidacy__job__pro': self.request.user.pro,
        }
        queryset = CandidacyMessage.objects.filter(~Q(candidacy__status=Candidacy.MATCHING), **qs_filter)
        queryset = queryset.select_related('candidacy__applicant__user', 'emmiter')
        return queryset.distinct('candidacy__id').order_by('candidacy__id', '-created')

    def get_serializer_context(self):
        context = super(CandidacyMessageJobListAPIView, self).get_serializer_context()
        qs_filter = {
            'candidacy__job': self.kwargs.get('pk'),
            'candidacy__job__pro': self.request.user.pro,
        }
        reads = CandidacyMessageRead.objects.filter(**qs_filter)
        context['is_reads'] = {obj.candidacy_id: (obj.is_read, obj.date) for obj in reads}
        return context


class CandidacyMessageUnreadCountAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, IsProUser]

    def get(self, request):
        queryset = CandidacyMessageRead.objects.filter(~Q(candidacy__status=Candidacy.MATCHING))
        queryset = queryset.filter(candidacy__job__pro=request.user.pro, is_read=False)
        return Response({
            'unread_count': queryset.count(),
        })


class CandidacyMessageNotificationAPIView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsProUser]
    serializer_class = CandidacyMessageJobListSerializer
    pagination_class = CandidacyMessagesNotificationPagination

    def get_queryset(self):
        qs_filter = {
            'candidacy__job__pro': self.request.user.pro,
        }
        queryset = CandidacyMessage.objects.filter(~Q(candidacy__status=Candidacy.MATCHING), **qs_filter)
        queryset = queryset.select_related('candidacy__applicant__user', 'emmiter')
        return queryset.distinct('candidacy__id').order_by('candidacy__id', '-created')

    def get_serializer_context(self):
        context = super(CandidacyMessageNotificationAPIView, self).get_serializer_context()
        qs_filter = {
            'candidacy__job__pro': self.request.user.pro,
        }
        reads = CandidacyMessageRead.objects.filter(**qs_filter)
        context['is_reads'] = {obj.candidacy_id: (obj.is_read, obj.date) for obj in reads}
        return context
