# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from apps.core.api.pagination import CustomPagination, CustomCursorPagination


class CandidacyJobMessagePagination(CustomPagination):
    page_size = 10


class CandidacyMessagesPagination(CustomCursorPagination):
    page_size = 6


class CandidacyMessagesNotificationPagination(CustomPagination):
    page_size = 5
