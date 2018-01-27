# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from django.contrib.auth.models import Group
from django.core.exceptions import ImproperlyConfigured
from django.utils.six import text_type


class BaseAPITestCase(APITestCase):
    LIST_SUFFIX_URL = '-list'
    DETAIL_SUFFIX_URL = '-detail'
    LOOKUP_FIELD = 'pk'

    base_name = None
    factory_class = None
    serializer_class = None
    user_factory_class = None

    def get_factory_class(self):
        return getattr(self, 'factory_class')

    def get_object(self, factory, **kwargs):
        return factory.create(**kwargs)

    def generate_object(self, **kwargs):
        return self.get_object(self.get_factory_class(), **kwargs)

    def get_user_factory_class(self):
        return getattr(self, 'user_factory_class')

    def get_user(self, factory, **kwargs):
        return factory.create(**kwargs)

    def generate_user(self, **kwargs):
        return self.get_user(self.get_user_factory_class(), **kwargs)

    def get_serializer_class(self):
        if self.serializer_class is None:
            raise ImproperlyConfigured('"%s" should either include a `serializer_class` attribute,'
                                       'or override the `get_serializer_class()` method.' % self.__class__.__name__)
        return self.serializer_class

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)

    def authenticate_user(self):
        self.user = self.generate_user()
        self.client.force_authenticate(self.user)

    def add_group_to_user(self, name):
        self.user.groups.add(Group.objects.get(name=name))


class ListAPITestCaseMixin(object):
    nb_objects_to_generate = 5

    def get_list_url(self):
        return reverse(self.base_name + self.LIST_SUFFIX_URL)

    def get_list_response(self, **kwargs):
        return self.client.get(self.get_list_url(), **kwargs)

    def generate_objects(self, **kwargs):
        return [self.generate_object(**kwargs) for i in range(self.nb_objects_to_generate)]


class RetrieveAPITestCaseMixin(object):
    def get_retrieve_url(self):
        object_id = getattr(self.object, self.LOOKUP_FIELD)
        return reverse(self.base_name + self.DETAIL_SUFFIX_URL, args=[text_type(object_id)])

    def get_retrieve_response(self, **kwargs):
        return self.client.get(self.get_retrieve_url(), **kwargs)


class CreateAPITestCaseMixin(object):
    def get_create_url(self):
        return reverse(self.base_name + self.LIST_SUFFIX_URL)

    def get_create_response(self, data=None, **kwargs):
        data = data or {}
        return self.client.post(self.get_create_url(), data, **kwargs)


class UpdateAPITestCaseMixin(object):
    def get_update_url(self):
        self.object_id = getattr(self.object, self.LOOKUP_FIELD)
        return reverse(self.base_name + self.DETAIL_SUFFIX_URL, args=[text_type(self.object_id)])

    def get_update_response(self, data=None, results=None, use_patch=True, **kwargs):
        args = [self.get_update_url(), data]
        return self.client.patch(*args, **kwargs) if use_patch else self.client.put(*args, **kwargs)


class DestroyAPITestCaseMixin(object):
    def get_destroy_url(self):
        self.object_id = getattr(self.object, self.LOOKUP_FIELD)
        return reverse(self.base_name + self.DETAIL_SUFFIX_URL, args=[text_type(self.object_id)])

    def get_destroy_response(self, **kwargs):
        return self.client.delete(self.get_destroy_url(), **kwargs)
