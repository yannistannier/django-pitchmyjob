# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from rest_framework import serializers

from django.db.models import Q
from django.utils.translation import ugettext as _

from apps.authentication.api.serializers import UserSerializer

from ..models import CandidacyMessage, CandidacyMessageRead


class CandidacyMessageSerializer(serializers.ModelSerializer):
    emmiter = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    emmiter_extra = UserSerializer(source='emmiter', read_only=True)

    class Meta:
        model = CandidacyMessage
        fields = ('id', 'candidacy', 'emmiter', 'emmiter_extra', 'message', 'created')
        read_only_fields = ('id', 'created')

    def validate_candidacy(self, value):
        request = self.context.get('request')
        if request.user.is_pro and value.job.pro != request.user.pro:
            raise serializers.ValidationError(_('La candidature ne correspond pas à une offre de votre structure'))
        elif request.user.is_applicant and value.applicant != request.user.applicant:
            raise serializers.ValidationError(_('La candidature ne vous est pas liée'))
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        candidacy = validated_data.get('candidacy')
        CandidacyMessageRead.objects.filter(Q(candidacy=candidacy) & ~Q(user=request.user)).update(is_read=False)
        return super(CandidacyMessageSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        del validated_data['candidacy']  # Remove candidacy from validated_data to avoid updating it
        return super(CandidacyMessageSerializer, self).update(instance, validated_data)


class CandidacyMessageJobListSerializer(serializers.ModelSerializer):
    applicant = UserSerializer(source='candidacy.applicant.user', read_only=True)
    emmiter = UserSerializer(read_only=True)
    job = serializers.PrimaryKeyRelatedField(source='candidacy.job.id', read_only=True)
    is_read = serializers.SerializerMethodField()

    class Meta:
        model = CandidacyMessage
        fields = ('id', 'candidacy', 'applicant', 'job', 'emmiter', 'message', 'created', 'is_read')

    def get_is_read(self, obj):
        is_read = self.context.get('is_reads').get(obj.candidacy_id)
        if is_read:
            return {'is_read': is_read[0], 'date': is_read[1]}
        return {'is_read': False, 'date': None}
