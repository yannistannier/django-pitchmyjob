# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import os

from unipath import Path

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _


def get_env_variable(var_name):
    """
    Get the environment variable or return exception
    """
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = 'Set the {0} environment variable'.format(var_name)
        raise ImproperlyConfigured(error_msg)


BASE_DIR = Path(__file__).ancestor(2)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_variable('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ADMINS = [
    ('Tannier Yannis', 'tannier.yannis@gmail.com'),
]

MANAGERS = ADMINS

DEFAULT_FROM_EMAIL = 'xxxxxxx'

SITE_ID = 1

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Thirds apps
    'rest_framework',
    'rest_framework.authtoken',
    'storages',
    'rest_framework_docs',
    # Own apps
    'apps.core.apps.CoreConfig',
    'apps.applicant.apps.ApplicantConfig',
    'apps.authentication.apps.AuthenticationConfig',
    'apps.candidacy.apps.CandidacyConfig',
    'apps.pro.apps.ProConfig',
    'apps.data.apps.DataConfig',
    'apps.job.apps.JobConfig',
    'apps.notification.apps.NotificationConfig',
    'apps.message.apps.MessageConfig',
]

MIDDLEWARE = [
    # Django middlewares
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'fr-fr'

LANGUAGES = [
    ('fr', _('French')),
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AWS_ACCESS_KEY_ID = get_env_variable('AWS_ACCESS_KEY_ID')

AWS_SECRET_ACCESS_KEY = get_env_variable('AWS_SECRET_ACCESS_KEY')

AWS_STORAGE_BUCKET_NAME = 'spitchapp-dev'

STATICFILES_STORAGE = 'apps.core.storages.StaticStorage'

DEFAULT_FILE_STORAGE = 'apps.core.storages.MediaStorage'

AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

STATICFILES_LOCATION = 'barney/static'

STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)

STATIC_ROOT = BASE_DIR.child('static')

MEDIAFILES_LOCATION = 'barney/media'

MEDIA_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)

MEDIA_ROOT = BASE_DIR.child('media')

AUTH_USER_MODEL = 'authentication.User'

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'EXCEPTION_HANDLER': 'apps.core.api.utils.custom_exception_handler',
}

DAYS_JOB = 30

REGISTER_CONFIRMATION = True

MATCHING_LAMBDA = "matching-Job"
