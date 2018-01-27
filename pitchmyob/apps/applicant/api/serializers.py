# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from rest_framework import serializers

from apps.authentication.api.serializers import UserSerializer

from ..models import (Applicant, ApplicantExperience, ApplicantEducation, ApplicantSkill, ApplicantLanguage,
                      ApplicantInterest)
from .fields import CurrentApplicantDefault


class ApplicantExperienceSerializer(serializers.ModelSerializer):
    applicant = serializers.PrimaryKeyRelatedField(read_only=True, default=CurrentApplicantDefault())

    class Meta:
        model = ApplicantExperience
        fields = '__all__'


class ApplicantEducationSerializer(serializers.ModelSerializer):
    applicant = serializers.PrimaryKeyRelatedField(read_only=True, default=CurrentApplicantDefault())

    class Meta:
        model = ApplicantEducation
        fields = '__all__'


class ApplicantSkillSerializer(serializers.ModelSerializer):
    applicant = serializers.PrimaryKeyRelatedField(read_only=True, default=CurrentApplicantDefault())

    class Meta:
        model = ApplicantSkill
        fields = '__all__'


class ApplicantLanguageSerializer(serializers.ModelSerializer):
    applicant = serializers.PrimaryKeyRelatedField(read_only=True, default=CurrentApplicantDefault())

    class Meta:
        model = ApplicantLanguage
        fields = '__all__'


class ApplicantInterestSerializer(serializers.ModelSerializer):
    applicant = serializers.PrimaryKeyRelatedField(read_only=True, default=CurrentApplicantDefault())

    class Meta:
        model = ApplicantInterest
        fields = '__all__'


class ApplicantFullSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    experiences = ApplicantExperienceSerializer(many=True, read_only=True)
    educations = ApplicantEducationSerializer(many=True, read_only=True)
    skills = ApplicantSkillSerializer(many=True, read_only=True)
    languages = ApplicantLanguageSerializer(many=True, read_only=True)
    interests = ApplicantInterestSerializer(many=True, read_only=True)

    class Meta:
        model = Applicant
        fields = '__all__'


class ApplicantMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        exclude = ('user',)
