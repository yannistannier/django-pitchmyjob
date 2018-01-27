# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User
from apps.event.mixins import EventAuthAdminMixin


# admin.site.register(User, UserAdmin)

@admin.register(User)
class UserAdmin(EventAuthAdminMixin, UserAdmin):
    pass
