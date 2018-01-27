# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import factory

from django.utils import timezone

from apps.pro.factories import ProFactory

from .models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'username %d' % n)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.LazyAttributeSequence(lambda o, n: '%s%s%d@pitch.com' % (o.first_name, o.last_name, n))
    is_staff = False
    is_active = True
    date_joined = factory.LazyFunction(timezone.now)
    pro = None


class UserProFactory(UserFactory):
    pro = factory.SubFactory(ProFactory)
