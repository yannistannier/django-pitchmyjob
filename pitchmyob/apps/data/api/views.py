# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from ..models import Industry, Employee, ContractType, Experience, StudyLevel
from .serializers import (IndustrySerializer, EmployeeSerializer, ContractTypeSerializer, ExperienceSerializer,
                          StudyLevelSerializer)


class IndustryViewSet(ListModelMixin, GenericViewSet):
    queryset = Industry.objects.filter(is_active=True)
    serializer_class = IndustrySerializer


class EmployeeViewSet(ListModelMixin, GenericViewSet):
    queryset = Employee.objects.filter(is_active=True)
    serializer_class = EmployeeSerializer


class ContractTypeViewSet(ListModelMixin, GenericViewSet):
    queryset = ContractType.objects.filter(is_active=True)
    serializer_class = ContractTypeSerializer


class ExperienceViewSet(ListModelMixin, GenericViewSet):
    queryset = Experience.objects.filter(is_active=True)
    serializer_class = ExperienceSerializer


class StudyLevelViewSet(ListModelMixin, GenericViewSet):
    queryset = StudyLevel.objects.filter(is_active=True)
    serializer_class = StudyLevelSerializer
