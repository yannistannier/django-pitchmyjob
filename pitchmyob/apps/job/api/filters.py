# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import django_filters

from ..models import Job


class JobFilter(django_filters.rest_framework.FilterSet):
    is_pending = django_filters.CharFilter(method='get_is_pending')
    is_visible = django_filters.CharFilter(method='get_is_visible')
    is_expired = django_filters.CharFilter(method='get_is_expired')

    class Meta:
        model = Job
        fields = ('is_pending', 'is_visible', 'is_expired')

    def get_is_pending(self, queryset, name, value):
        return queryset.is_pending()

    def get_is_visible(self, queryset, name, value):
        return queryset.is_visible()

    def get_is_expired(self, queryset, name, value):
        return queryset.is_expired()
