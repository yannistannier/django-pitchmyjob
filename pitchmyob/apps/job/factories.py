# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import random

import factory

from apps.core.factories import LocalisationFactoryMixin
from apps.pro.factories import ProFactory

from .models import Job, JobQuestion


class JobFactory(LocalisationFactoryMixin, factory.django.DjangoModelFactory):
    class Meta:
        model = Job

    pro = factory.SubFactory(ProFactory)
    title = factory.Sequence(lambda n: 'Job n°%d' % n)
    salary = factory.LazyAttribute(lambda o: random.randint(22000, 50000))
    skills = ['Compétence 1', 'Coméptence 2', 'Coméptence 3']
    description = factory.Faker('text')
    view_counter = factory.LazyAttribute(lambda o: random.randint(0, 100))
    last_payment = None
    is_active = True

    @factory.post_generation
    def contract_types(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for contract_type in extracted:
                self.contract_types.add(contract_type)

    @factory.post_generation
    def experiences(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for experience in extracted:
                self.experiences.add(experience)

    @factory.post_generation
    def study_levels(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for study_level in extracted:
                self.study_levels.add(study_level)


class JobQuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = JobQuestion

    job = factory.SubFactory(JobFactory)
    question = factory.Sequence(lambda n: 'Question n°%d' % n)
    order = 1
