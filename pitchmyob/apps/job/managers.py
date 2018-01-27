# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import datetime

from django.conf import settings
from django.db import models
from django.utils import timezone


class JobQuerySet(models.QuerySet):
    def is_pending(self):
        return self.filter(last_payment__isnull=True)

    def is_visible(self):
        date = timezone.now() - datetime.timedelta(days=settings.DAYS_JOB)
        return self.filter(last_payment__gte=date)

    def is_expired(self):
        date = timezone.now() - datetime.timedelta(days=settings.DAYS_JOB)
        return self.filter(last_payment__lt=date)


JobManager = models.Manager.from_queryset(JobQuerySet)()
