# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from rest_framework.authtoken.models import Token
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import get_object_or_404

from ..models import User


class AuthLoginMixin(object):
    login_type = None

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

    def get_serializer_context(self):
        if not self.login_type:
            raise ImproperlyConfigured('"%s" should include a `login_type` attribute.' % self.__class__.__name__)
        return {'login_type': self.login_type}


class AuthRegisterConfirmMixin(object):
    token_field = None

    def get_object(self):
        email = self.request.data.get('email')
        token = self.request.data.get('token')
        if email and token:
            qs_filter = {
                'is_active': False,
                'email': email,
                self.token_field: token,
            }
            return get_object_or_404(User, **qs_filter)
        raise NotFound()
