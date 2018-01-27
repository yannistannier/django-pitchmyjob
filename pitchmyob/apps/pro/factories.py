# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import random

import factory

from apps.core.factories import LocalisationFactoryMixin
from apps.data.factories import IndustryFactory, EmployeeFactory

from .models import Pro


class ProFactory(LocalisationFactoryMixin, factory.django.DjangoModelFactory):
    class Meta:
        model = Pro

    company = factory.Faker('company')
    website = factory.Faker('url')
    description = factory.Faker('text')
    phone = factory.Faker('phone_number')
    industry = factory.SubFactory(IndustryFactory)
    employes = factory.SubFactory(EmployeeFactory)
    ca = factory.LazyAttribute(lambda o: random.randint(60000, 100000))
    logo = None
    is_active = True
