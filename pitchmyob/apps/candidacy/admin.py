# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib import admin

from .models import Candidacy, CandidacyComment


class CandidacyCommentInlineAdmin(admin.TabularInline):
    model = CandidacyComment
    fields = ('collaborator', 'message')
    extra = 0

    def has_add_permission(self, request):
        return False


@admin.register(Candidacy)
class CandidacyAdmin(admin.ModelAdmin):
    fields = ('job', 'applicant', 'collaborator', 'status', 'date_matching', 'date_like', 'date_request', 'date_video',
              'date_decision')
    list_display = ('job', 'applicant', 'status')
    list_filter = ('status',)
    search_fields = ('job__title', 'job__pro__company')
    inlines = [CandidacyCommentInlineAdmin]

    def has_add_permission(self, request):
        return False

    def get_readonly_fields(self, request, obj=None):
        return self.fields
