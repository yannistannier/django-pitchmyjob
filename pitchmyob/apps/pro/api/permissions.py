# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from rest_framework import permissions


class IsProUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_pro
