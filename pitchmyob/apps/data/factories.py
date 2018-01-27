# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import factory

from apps.core.management.commands import _data as sample_data
from .models import Industry, Employee, ContractType, Experience, StudyLevel


class DataFactoryMixin(factory.django.DjangoModelFactory):
    class Meta:
        abstract = True

    is_active = True
    order = factory.Sequence(int)


class IndustryFactory(DataFactoryMixin, factory.django.DjangoModelFactory):
    class Meta:
        model = Industry

    name = factory.Iterator(sample_data.INDUSTRIES)


class EmployeeFactory(DataFactoryMixin, factory.django.DjangoModelFactory):
    class Meta:
        model = Employee

    name = factory.Iterator(sample_data.EMPLOYEES)


class ContractTypeFactory(DataFactoryMixin, factory.django.DjangoModelFactory):
    class Meta:
        model = ContractType

    name = factory.Iterator(sample_data.CONTRACT_TYPES)


class ExperienceFactory(DataFactoryMixin, factory.django.DjangoModelFactory):
    class Meta:
        model = Experience

    name = factory.Iterator(sample_data.EXPERIENCES)


class StudyLevelFactory(DataFactoryMixin, factory.django.DjangoModelFactory):
    class Meta:
        model = StudyLevel

    name = factory.Iterator(sample_data.STUDY_LEVELS)
