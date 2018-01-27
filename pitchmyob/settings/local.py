# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from .base import *  # noqa


DEBUG = True

ALLOWED_HOSTS = ['*']

AUTH_PASSWORD_VALIDATORS = []

INSTALLED_APPS += [
    # Thirds apps
    'django_extensions',
    'corsheaders',
]

MIDDLEWARE = MIDDLEWARE + ['corsheaders.middleware.CorsMiddleware']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': get_env_variable('DJANGO_DB_DEV_HOST'),
        'NAME': get_env_variable('DJANGO_DB_DEV_NAME'),
        'USER': get_env_variable('DJANGO_DB_DEV_USER'),
        'PASSWORD': get_env_variable('DJANGO_DB_DEV_PASSWORD'),
    }
}

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EVENT_LOG = "EventLog-dev"

SNS_EMAIL = "arn:aws:sns:eu-west-1:xxxxxxx:sendEmail-dev"
SQS_EMAIL = "v2-sqsEmail-dev"

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = (
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS'
)

CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken'
)

REGISTER_CONFIRMATION = False
