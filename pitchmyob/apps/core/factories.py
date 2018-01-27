# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import factory


class LocalisationFactoryMixin(factory.django.DjangoModelFactory):
    class Meta:
        abstract = True

    address = factory.Faker('address')
    latitude = factory.Faker('latitude')
    longitude = factory.Faker('longitude')
    street_number = factory.Faker('building_number')
    route = factory.Faker('street_name')
    cp = factory.Faker('zipcode')
    locality = factory.Faker('city')
    administrative_area_level_1 = factory.Faker('state')
    administrative_area_level_2 = factory.Faker('state')
    country = factory.Faker('country')
