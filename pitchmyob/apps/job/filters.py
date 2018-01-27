# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Job


class StateListFilter(admin.SimpleListFilter):
    STATE_PENDING = 'pending'
    STATE_VISIBLE = 'visible'
    STATE_EXPIRED = 'expired'

    title = _('état')
    parameter_name = 'state'

    def lookups(self, request, model_admin):
        return (
            (self.STATE_PENDING, Job.STATE_PENDING_LABEL),
            (self.STATE_VISIBLE, Job.STATE_VISIBLE_LABEL),
            (self.STATE_EXPIRED, Job.STATE_EXPIRED_LABEL),
        )

    def queryset(self, request, queryset):
        if self.value() == self.STATE_PENDING:
            return queryset.is_pending()
        elif self.value() == self.STATE_VISIBLE:
            return queryset.is_visible()
        elif self.value() == self.STATE_EXPIRED:
            return queryset.is_expired()
