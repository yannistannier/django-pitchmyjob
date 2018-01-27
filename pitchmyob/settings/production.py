# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from .base import *  # noqa


DEBUG = False

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += [
    'raven.contrib.django.raven_compat',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': get_env_variable('DJANGO_DB_PROD_HOST'),
        'NAME': get_env_variable('DJANGO_DB_PROD_NAME'),
        'USER': get_env_variable('DJANGO_DB_PROD_USER'),
        'PASSWORD': get_env_variable('DJANGO_DB_PROD_PASSWORD'),
    }
}

RAVEN_CONFIG = {
    # a configurer
}

# AWS_STORAGE_BUCKET_NAME = '<to_define>'

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

REST_FRAMEWORK_DOCS = {
    'HIDE_DOCS': True
}

EVENT_LOG = "EventLog-production"

SNS_EMAIL = "arn:aws:sns:eu-west-1:xxxxxxx:sendEmail-production"

SQS_EMAIL = "v2-sqsEmail-production"

AWS_STORAGE_BUCKET_NAME = 'v2-pitchmyjob-production'
