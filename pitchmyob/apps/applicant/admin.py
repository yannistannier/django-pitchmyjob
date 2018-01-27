# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib import admin

from apps.event.mixins import EventApplicantAdminMixin
from .models import (Applicant, ApplicantExperience, ApplicantEducation, ApplicantSkill, ApplicantLanguage,
                     ApplicantInterest)


class ApplicantExperienceInlineAdmin(admin.TabularInline):
    model = ApplicantExperience
    fields = ('company', 'position', 'location', 'description')
    extra = 0


class ApplicantEducationInlineAdmin(admin.TabularInline):
    model = ApplicantEducation
    fields = ('school', 'degree', 'description')
    extra = 0


class ApplicantSkillInlineAdmin(admin.TabularInline):
    model = ApplicantSkill
    fields = ('name', 'level')
    extra = 0


class ApplicantLanguageInlineAdmin(admin.TabularInline):
    model = ApplicantLanguage
    fields = ('name', 'level')
    extra = 0


class ApplicantInterestInlineAdmin(admin.TabularInline):
    model = ApplicantInterest
    fields = ('name',)
    extra = 0


@admin.register(Applicant)
class ApplicantAdmin(EventApplicantAdminMixin, admin.ModelAdmin):
    fields = ('user', 'title', 'birthday', 'description', 'url', 'wanted_skills', 'wanted_jobs', 'wanted_contracts')
    readonly_fields = ('user',)
    filter_horizontal = ('wanted_contracts',)
    list_display = ('user', 'title')
    list_filter = ('wanted_contracts',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'title', 'wanted_skills', 'wanted_jobs')
    inlines = [ApplicantExperienceInlineAdmin, ApplicantEducationInlineAdmin, ApplicantSkillInlineAdmin,
               ApplicantLanguageInlineAdmin, ApplicantInterestInlineAdmin]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
