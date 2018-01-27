# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from rest_framework import permissions


class IsAuthenticatedMixin(object):
    permission_classes = [permissions.IsAuthenticated]


class IsActiveDestroyMixin(object):
    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
