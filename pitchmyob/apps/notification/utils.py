# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.db.models.query import QuerySet

from apps.core.utils import Email
from apps.candidacy.models import Candidacy, CandidacyComment
from apps.job.models import Job
from apps.message.models import CandidacyMessage

from .models import Notification


class NotificationHandler(object):
    def __init__(self, request, type_name, emmiter, action_object):
        self.request = request
        self.type_name = type_name
        self.emmiter = emmiter
        self.action_object = action_object

    def perform_applicant_candidacy_requested(self):
        receivers = self.action_object.applicant.user
        self.send_notifications(receivers)
        self.send_emails('Demande de candidature', receivers, 'applicant/candidacy_requested.html')

    def perform_applicant_candidacy_approved(self):
        receivers = self.action_object.applicant.user
        self.send_notifications(receivers)
        self.send_emails('Candidature validé', receivers, 'applicant/candidacy_approved.html')

    def perform_applicant_candidacy_disapproved(self):
        receivers = self.action_object.applicant.user
        self.send_notifications(receivers)
        self.send_emails('Candidature refusé', receivers, 'applicant/candidacy_disapproved.html')

    def perform_pro_job_added(self):
        receivers = self.action_object.pro.user_set.filter(is_active=True).filter(~Q(pk=self.request.user.pk))
        self.send_notifications(receivers)
        self.send_emails('Offre ajoutée', receivers, 'pro/job_added.html')

    def perform_pro_job_updated(self):
        receivers = self.action_object.pro.user_set.filter(is_active=True).filter(~Q(pk=self.request.user.pk))
        self.send_notifications(receivers)
        self.send_emails('Offre modifiée', receivers, 'pro/job_updated.html')

    def perform_pro_job_published(self):
        receivers = self.action_object.pro.user_set.filter(is_active=True).filter(~Q(pk=self.request.user.pk))
        self.send_notifications(receivers)
        self.send_emails('Offre publiée', receivers, 'pro/job_published.html')

    def perform_pro_job_deleted(self):
        receivers = self.action_object.pro.user_set.filter(is_active=True).filter(~Q(pk=self.request.user.pk))
        self.send_notifications(receivers)
        self.send_emails('Offre supprimée', receivers, 'pro/job_deleted.html')

    def perform_pro_job_liked(self):
        receivers = self.action_object.job.pro.user_set.filter(is_active=True)
        self.send_notifications(receivers)
        self.send_emails('Offre aimée', receivers, 'pro/job_liked.html')

    def perform_pro_job_new_candidacy(self):
        receivers = self.action_object.applicant.user
        self.send_emails('Confirmation candidature', receivers, 'applicant/job_new_candidacy.html')

        receivers = self.action_object.job.pro.user_set.filter(is_active=True)
        self.send_notifications(receivers)
        self.send_emails('Nouvelle candidature', receivers, 'pro/job_new_candidacy.html')

    def perform_pro_collaborator_added(self):
        receivers = self.action_object.pro.user_set.filter(is_active=True).filter(~Q(pk=self.request.user.pk))
        self.send_notifications(receivers)
        self.send_emails('Nouveau collaborateur', receivers, 'pro/collaborator_added.html')

    def perform_pro_collaborator_deleted(self):
        receivers = self.action_object.pro.user_set.filter(is_active=True).filter(~Q(pk=self.request.user.pk))
        self.send_notifications(receivers)
        self.send_emails('Offre ajoutée', receivers, 'pro/collaborator_dele.html')

    def perform_new_message(self):
        emmiter_is_pro = self.action_object.emmiter.is_pro

        if not emmiter_is_pro:
            receivers = self.action_object.candidacy.job.pro.user_set.filter(is_active=True)
            self.send_emails('Nouveau message', receivers, 'applicant/candidacy_new_message.html')
        else:
            qs_receivers = self.action_object.candidacy.job.pro.user_set.filter(is_active=True)
            receivers = list(qs_receivers.filter(~Q(pk=self.request.user.pk)))
            receivers += [self.action_object.candidacy.applicant.user]
            self.send_emails('Nouveau message', receivers, 'pro/candidacy_new_message.html')

    def perform_pro_candidacy_new_comment(self):
        receivers = self.action_object.candidacy.job.pro.user_set.filter(
            Q(is_active=True) & ~Q(pk=self.request.user.pk)
        )
        self.send_notifications(receivers)
        self.send_emails('Nouveau commentaire', receivers, 'pro/candidacy_new_comment.html')

    def send(self):
        method_name = 'perform_{}'.format(self.type_name).lower()
        method = getattr(self, method_name, None)
        if method:
            method()

    def get_receivers(self, receivers):
        if isinstance(receivers, QuerySet):
            return list(receivers.all())
        elif not isinstance(receivers, list):
            return [receivers]
        return receivers

    def send_notifications(self, receivers):
        action_object_content_type = ContentType.objects.get_for_model(self.action_object.__class__)

        instances = []
        for receiver in self.get_receivers(receivers):
            instances.append(Notification(type_name=self.type_name, emmiter=self.emmiter, receiver=receiver,
                                          action_object_content_type=action_object_content_type,
                                          action_object_id=self.action_object.pk))
        return Notification.objects.bulk_create(instances)

    def transform_action_object_to_context(self):
        if isinstance(self.action_object, Candidacy):
            return {
                'job': {
                    'title': self.action_object.job.title,
                    'company': self.action_object.job.pro.company
                }
            }
        elif isinstance(self.action_object, CandidacyComment):
            return {}
        elif isinstance(self.action_object, Job):
            return {
                'id': self.action_object.id,
                'title': self.action_object.title,
                'company': self.action_object.pro.company,
                'logo': self.action_object.pro.logo.url,
                'location': {
                    'country': self.action_object.country,
                    'locality': self.action_object.locality
                }
            }
        elif isinstance(self.action_object, CandidacyMessage):
            return {
                'id': self.action_object.id,
                'candidacy_id': self.action_object.candidacy.id,
                'job': self.action_object.candidacy.job.title,
                'emmiter': {
                    'first_name': self.action_object.emmiter.first_name,
                    'last_name': self.action_object.emmiter.last_name,
                    'photo': self.action_object.emmiter.photo.url,
                }
            }
        return {}

    def send_emails(self, subject, receivers, template):
        for receiver in self.get_receivers(receivers):
            context = {
                'user': {
                    'name': receiver.get_full_name(),
                    'first_name': receiver.first_name,
                    'last_name': receiver.last_name,
                    'email': receiver.email,
                    'photo': receiver.photo.url,
                },
                'action_object': self.transform_action_object_to_context(),
            }
            Email(subject=subject, to=receiver, context=context, template=template).send()
