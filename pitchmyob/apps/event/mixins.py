# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.forms.models import model_to_dict

from .core import CoreEventJob, CoreEventApplicant, CoreMatchingEvent
from apps.applicant.models import (ApplicantExperience, ApplicantEducation, ApplicantSkill, ApplicantLanguage,
                                   ApplicantInterest)


class EventApplicantViewSetMixin(CoreEventApplicant):

    def perform_create(self, serializer):
        super(EventApplicantViewSetMixin, self).perform_create(serializer)
        if self.event_type == "applicant":
            self.applicant_id = serializer.instance.applicant.id
        self.create_dict_to_push(serializer.validated_data)
        self.topush["id"] = serializer.instance.id
        self.push_event("add")

    def perform_update(self, serializer):
        super(EventApplicantViewSetMixin, self).perform_update(serializer)
        if self.request.user.is_applicant:
            self.create_dict_to_push(serializer.validated_data)
            self.topush["id"] = serializer.instance.id
            self.push_event("edit")

    def perform_destroy(self, serializer):
        self.topush = {"id": self.get_object().id}
        self.push_event("delete")
        super(EventApplicantViewSetMixin, self).perform_destroy(serializer)


class EventApplicantAdminMixin(CoreEventApplicant):

    def define_event_type(self, instance):
        if isinstance(instance, ApplicantExperience):
            self.event_type = "experience"
        if isinstance(instance, ApplicantEducation):
            self.event_type = "education"
        if isinstance(instance, ApplicantSkill):
            self.event_type = "skill"
        if isinstance(instance, ApplicantLanguage):
            self.event_type = "language"
        if isinstance(instance, ApplicantInterest):
            self.event_type = "interest"

    def save_formset(self, request, form, formset, change):
        for instance in formset.save(commit=False):
            action = "edit" if instance.id else "add"
            instance.save()
            self.define_event_type(instance)
            self.create_dict_to_push(model_to_dict(instance))
            self.topush["id"] = instance.id
            self.push_event(action)

        for instance in formset.deleted_objects:
            self.define_event_type(instance)
            self.topush = {'id': instance.id}
            self.push_event("delete")
            instance.delete()

    def save_model(self, request, obj, form, change):
        super(EventApplicantAdminMixin, self).save_model(request, obj, form, change)
        self.applicant_id = obj.id
        changed = {c: form.cleaned_data[c] for c in form.changed_data}
        if change and changed:
            self.topush = {}
            self.create_dict_to_push(changed)
            self.event_type = "applicant"
            self.topush["id"] = self.applicant_id
            self.push_event("edit")


class EventAuthAdminMixin(CoreEventApplicant):
    accepted_fields = [
        "first_name",
        "last_name",
        "email",
        "photo",
        "is_active"
    ]

    def save_model(self, request, obj, form, change):
        super(EventAuthAdminMixin, self).save_model(request, obj, form, change)
        if obj.is_applicant:
            changed = {c: form.cleaned_data[c] for c in form.changed_data if c in self.accepted_fields}
            self.event_type = "applicant"
            self.applicant_id = obj.applicant.id

            if obj.is_active and "is_active" in changed:
                self.topush = {k: str(v) for k, v in model_to_dict(obj).items() if k in self.accepted_fields}
                self.topush["id"] = obj.applicant.id
                self.push_event("add")

            if obj.is_active and "is_active" not in changed:
                self.create_dict_to_push(changed)
                self.topush["id"] = obj.applicant.id
                self.push_event("edit")

            if not obj.is_active and "is_active" in changed:
                self.push_event("delete")


class EventJobAdminMixin(CoreEventJob):

    def delete_model(self, request, object):
        self.job_id = object.id
        self.push_event("delete_job")
        super(EventJobAdminMixin, self).delete_model(request, object)

    def save_model(self, request, obj, form, change):
        super(EventJobAdminMixin, self).save_model(request, obj, form, change)
        changed = {c: form.cleaned_data[c] for c in form.changed_data}
        self.job_id = obj.id

        # On update une offre qui est deja active et publier
        if obj.last_payment and change and "last_payment" not in changed and obj.is_active and \
           "is_active" not in changed:
            self.dict_to_push(changed)
            self.push_event("edit_job")

        # on republie une offre qui a deja paye mais qui a ete depublier une fois
        if obj.last_payment and change and "last_payment" not in changed and obj.is_active and "is_active" in changed:
            self.initial_dict_to_push(obj)
            self.push_event("add_job")

        # On publie un job deja existance et active => event add en lui envoyant tout job
        if obj.last_payment and change and "last_payment" in changed and obj.is_active:
            self.initial_dict_to_push(obj)
            self.push_event("add_job")

        # On cree et on publie pour la premiere fois une offre
        if not change and obj.last_payment and obj.is_active:
            self.initial_dict_to_push(obj)
            self.push_event("add_job")

        # On desative une offre deja publique deja paye
        if change and not obj.is_active and changed and "is_active" in changed:
            self.push_event("delete_job")


class EventJobViewSetMixin(CoreEventJob, CoreMatchingEvent):

    def perform_update(self, serializer):
        old_object = self.get_object()
        super(EventJobViewSetMixin, self).perform_update(serializer)
        new_object = serializer.instance

        if new_object.last_payment:
            self.job_id = new_object.id
            if old_object.last_payment:
                self.dict_to_push(serializer.validated_data)
                self.push_event("edit_job")
            else:
                self.initial_dict_to_push(serializer.instance)
                self.push_event("add_job")
                self.object_id = self.job_id
                self.push_matching("match_job")

    def perform_destroy(self, serializer):
        self.job_id = self.get_object().id
        self.push_event("delete_job")
        super(EventJobViewSetMixin, self).perform_destroy(serializer)
