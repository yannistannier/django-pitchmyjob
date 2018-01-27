# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from rest_framework import serializers

from django.utils import timezone
from django.utils.translation import ugettext as _

from apps.applicant.api.serializers import ApplicantFullSerializer
from apps.authentication.api.serializers import UserSerializer
from apps.job.api.serializers import JobFullSerializer, ValidateJobSerializer

from ..models import Candidacy, CandidacyComment


class CandidacyProReadSerializer(serializers.ModelSerializer):
    applicant = ApplicantFullSerializer()

    class Meta:
        model = Candidacy
        fields = ('id', 'applicant', 'status', 'date_matching', 'date_like', 'date_request', 'date_video',
                  'date_decision')


class CandidacyProResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidacy
        fields = ('id', 'job', 'applicant', 'status')


class CandidacyProRequestSerializer(ValidateJobSerializer, serializers.ModelSerializer):
    class Meta:
        model = Candidacy
        fields = ('id', 'job', 'applicant', 'status')
        read_only_fields = ('id', 'status',)

    def get_validated_data(self, validated_data):
        validated_data.update({
            'collaborator': self.context.get('request').user,
            'status': Candidacy.REQUEST,
            'date_request': timezone.now(),
        })
        return validated_data

    def create(self, validated_data):
        return super(CandidacyProRequestSerializer, self).create(self.get_validated_data(validated_data))

    def update(self, instance, validated_data):
        return super(CandidacyProRequestSerializer, self).update(instance, self.get_validated_data(validated_data))


class CandidacyProActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidacy
        fields = ('id', 'job', 'applicant', 'status')
        read_only_fields = ('job', 'applicant', 'status')

    def update(self, instance, validated_data):
        return super(CandidacyProActionSerializer, self).update(instance, {
            'status': self.status_value,
            'date_decision': timezone.now()
        })


class CandidacyProApproveSerializer(CandidacyProActionSerializer):
    status_value = Candidacy.SELECTED


class CandidacyProDisapproveSerializer(CandidacyProActionSerializer):
    status_value = Candidacy.NOT_SELECTED


class CandidacyApplicantReadSerializer(serializers.ModelSerializer):
    job = JobFullSerializer()

    class Meta:
        model = Candidacy
        fields = ('id', 'job', 'status', 'date_matching', 'date_like', 'date_request', 'date_video', 'date_decision',
                  'matching_score')


class CandidacyApplicantActionSerializer(CandidacyProActionSerializer):
    class Meta:
        model = Candidacy
        fields = ('job', 'applicant', 'status')
        read_only_fields = ('job', 'applicant', 'status')

    def update(self, instance, validated_data):
        return super(CandidacyApplicantActionSerializer, self).update(instance, {
            'status': self.status_value,
            self.date_field: timezone.now()
        })


class CandidacyApplicantLikeSerializer(CandidacyApplicantActionSerializer):
    status_value = Candidacy.LIKE
    date_field = 'date_like'


class CandidacyApplicantVideoSerializer(CandidacyApplicantActionSerializer):
    status_value = Candidacy.VIDEO
    date_field = 'date_video'


class CandidacyProCommentSerializer(serializers.ModelSerializer):
    collaborator = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    collaborator_extra = UserSerializer(source='collaborator', read_only=True)

    class Meta:
        model = CandidacyComment
        fields = ('id', 'candidacy', 'collaborator', 'collaborator_extra', 'message', 'created')
        read_only_fields = ('id',)

    def validate_candidacy(self, value):
        request = self.context.get('request')
        if value.job.pro != request.user.pro:
            raise serializers.ValidationError(_('La candidature ne correspond pas à une offre de votre structure'))
        return value
