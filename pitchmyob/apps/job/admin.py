# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib import admin

from .filters import StateListFilter
from .models import Job, JobQuestion
from apps.event.mixins import EventJobAdminMixin


class JobQuestionInlineAdmin(admin.TabularInline):
    model = JobQuestion
    fields = ('job', 'question', 'order')
    extra = 0


@admin.register(Job)
class JobAdmin(EventJobAdminMixin, admin.ModelAdmin):
    readonly_fields = ('view_counter',)
    filter_horizontal = ('contract_types', 'experiences', 'study_levels')
    list_display = ('pro', 'title', 'is_active', 'get_state', 'last_payment')
    list_filter = (StateListFilter, 'is_active', 'contract_types', 'experiences', 'study_levels')
    search_fields = ('title', 'skills', 'description')
    inlines = [JobQuestionInlineAdmin]
