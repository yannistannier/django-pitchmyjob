# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib import admin

from .models import Pro


@admin.register(Pro)
class ProAdmin(admin.ModelAdmin):
    fields = ('company', 'logo', 'industry', 'employes', 'ca', 'phone', 'website', 'description', 'is_active')
    list_display = ('company', 'industry', 'employes', 'ca', 'phone', 'website', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('company', 'description')
