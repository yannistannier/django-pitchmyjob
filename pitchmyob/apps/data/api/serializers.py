# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from rest_framework import serializers

from ..models import Industry, Employee, ContractType, Experience, StudyLevel


class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = ('id', 'name')


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'name')


class ContractTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractType
        fields = ('id', 'name')


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ('id', 'name')


class StudyLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyLevel
        fields = ('id', 'name')
