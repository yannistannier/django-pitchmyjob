# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from apps.core.api.pagination import CustomPagination


class JobPagination(CustomPagination):
    page_size = 10
