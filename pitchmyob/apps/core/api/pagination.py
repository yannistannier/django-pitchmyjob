# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from collections import OrderedDict

try:
    from urllib.parse import urlparse, parse_qs
except ImportError:
    from urlparse import urlparse, parse_qs

from rest_framework.pagination import PageNumberPagination, CursorPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('num_pages', self.page.paginator.num_pages),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


class CustomCursorPagination(CursorPagination):
    def get_paginated_response(self, data):
        next_link = self.get_next_link()
        previous_link = self.get_previous_link()

        # Retrieves next / previous cursor from next / previous links
        next_cursor = parse_qs(urlparse(next_link).query)['cursor'][0] if next_link else None
        previous_cursor = parse_qs(urlparse(previous_link).query)['cursor'][0] if previous_link else None

        return Response(OrderedDict([
            ('next', next_link),
            ('previous', previous_link),
            ('next_cursor', next_cursor),
            ('previous_cursor', previous_cursor),
            ('results', data)
        ]))
