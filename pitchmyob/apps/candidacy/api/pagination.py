# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from apps.core.api.pagination import CustomPagination, CustomCursorPagination


class CandidacyListPagination(CustomPagination):
    page_size = 10


class CandidacyCommentsPagination(CustomCursorPagination):
    page_size = 6
