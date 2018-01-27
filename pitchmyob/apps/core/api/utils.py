# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from django.http import Http404

from rest_framework.exceptions import ValidationError, PermissionDenied, NotFound
from rest_framework.views import exception_handler


def custom_exception_handler(exception, context):
    if isinstance(exception, DjangoPermissionDenied):
        exception = PermissionDenied()
    elif isinstance(exception, Http404):
        exception = NotFound()

    response = exception_handler(exception, context)

    if response is not None:
        if isinstance(exception, ValidationError):
            response.data = {
                'error': 'validation_error',
                'error_description': {},
            }

            field_errors = exception.detail
            for field_name, errors in field_errors.items():
                response.data['error_description'][field_name] = ' '.join(errors)
        else:
            details = exception.get_full_details()
            response.data = {
                'error': details.get('code'),
                'error_description': details.get('message'),
            }

    return response
