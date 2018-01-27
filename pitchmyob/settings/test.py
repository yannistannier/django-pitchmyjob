# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from .base import *  # noqa


INSTALLED_APPS += [
    # Thirds apps
    'django_jenkins',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': get_env_variable('DJANGO_DB_DEV_HOST'),
        'NAME': get_env_variable('DJANGO_DB_DEV_NAME'),
        'USER': get_env_variable('DJANGO_DB_DEV_USER'),
        'PASSWORD': get_env_variable('DJANGO_DB_DEV_PASSWORD'),
    }
}


EVENT_LOG = "EventLog-dev"

SNS_EMAIL = "arn:aws:sns:eu-west-1:xxxxxxxx:sendEmail-dev"
SQS_EMAIL = "v2-sqsCronEmail-dev"
