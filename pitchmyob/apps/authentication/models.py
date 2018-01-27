# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from apps.core.fields import ImageField


@python_2_unicode_compatible
class User(AbstractUser):
    DEFAULT_PHOTO = 'user/photo/default.jpg'

    username = models.CharField(_('username'), max_length=250, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    photo = ImageField(_('photo'), blank=True, default=DEFAULT_PHOTO)
    phone = models.CharField(_('numéro de téléphone'), max_length=250, default='')
    position = models.CharField(_('poste occupé'), max_length=250, default='')
    pro = models.ForeignKey('pro.Pro', blank=True, null=True, verbose_name=_('pro'))
    lost_password_token = models.CharField(_('jeton mot de passe perdu'), max_length=36, blank=True)
    confirm_email_token = models.CharField(_('jeton email'), max_length=36, blank=True)
    confirm_phone_token = models.CharField(_('jeton téléphone'), max_length=6, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    @cached_property
    def is_pro(self):
        return self.pro_id is not None

    @cached_property
    def is_applicant(self):
        return hasattr(self, 'applicant')
