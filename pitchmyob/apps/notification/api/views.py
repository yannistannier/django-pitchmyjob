# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from rest_framework import decorators
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.core.api.mixins import IsAuthenticatedMixin

from ..models import Notification
from .pagination import NotificationPagination
from .serializers import NotificationSerializer


class NotificationViewSet(IsAuthenticatedMixin, ListModelMixin, GenericViewSet):
    serializer_class = NotificationSerializer
    pagination_class = NotificationPagination
    filter_fields = ('is_unread',)

    def get_queryset(self):
        return Notification.objects.filter(receiver=self.request.user)

    def list(self, request, *args, **kwargs):
        response = super(NotificationViewSet, self).list(request, args, **kwargs)
        return response

    @decorators.list_route(methods=['get'], url_path='unread-count')
    def unread_count(self, request, pk=None):
        return Response({
            'unread_count': Notification.objects.filter(receiver=self.request.user, is_unread=True).count(),
        })

    @decorators.list_route(methods=['put', 'patch'], url_path='mark-all-as-read')
    def mark_all_as_read(self, request, pk=None):
        Notification.objects.filter(receiver=request.user, is_unread=True).update(is_unread=False)
        return Response()

    @decorators.detail_route(methods=['put', 'patch'], url_path='mark-as-read')
    def mark_as_read(self, request, pk=None):
        Notification.objects.filter(receiver=request.user, is_unread=True, id=pk).update(is_unread=False)
        return Response()
