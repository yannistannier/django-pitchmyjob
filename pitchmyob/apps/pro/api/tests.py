# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from rest_framework import status
from rest_framework.reverse import reverse

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from apps.authentication.factories import UserProFactory
from apps.core.api import tests

from .serializers import ProSerializer
from ..factories import ProFactory


class ProAPITestCase(tests.RetrieveAPITestCaseMixin,
                     tests.UpdateAPITestCaseMixin,
                     tests.DestroyAPITestCaseMixin,
                     tests.BaseAPITestCase):
    factory_class = ProFactory
    user_factory_class = UserProFactory
    serializer_class = ProSerializer

    def get_url(self):
        return reverse('pro')

    def get_retrieve_url(self):
        return self.get_url()

    def get_update_url(self):
        return self.get_url()

    def get_destroy_url(self):
        return self.get_url()

    def setUp(self):
        handle_pro = Group.objects.create(name='handle_pro')
        content_type = ContentType.objects.get(app_label='pro', model='pro')
        handle_pro.permissions.add(Permission.objects.get(content_type=content_type, codename='change_pro'))
        handle_pro.permissions.add(Permission.objects.get(content_type=content_type, codename='delete_pro'))

    def test_retrieve_not_logged_in_status_code(self):
        self.object = self.generate_object()
        response = self.get_retrieve_response()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_logged_in_status_code(self):
        self.user = self.generate_user()
        self.client.force_authenticate(self.user)
        self.object = self.user.pro
        response = self.get_retrieve_response()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_logged_in_content_returned(self):
        self.user = self.generate_user()
        self.add_group_to_user('handle_pro')
        self.client.force_authenticate(self.user)
        self.object = self.user.pro
        serializer = self.get_serializer(self.object)
        response = self.get_retrieve_response()
        self.assertEqual(response.data, serializer.data)

    def test_update_not_logged_in_status_code(self):
        self.object = self.generate_object()
        response = self.get_update_response(data={'company': 'New company'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_logged_in_no_perms_status_code(self):
        self.user = self.generate_user()
        self.client.force_authenticate(self.user)
        self.object = self.user.pro
        response = self.get_update_response(data={'company': 'New company'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_logged_in_has_perms_status_code(self):
        self.user = self.generate_user()
        self.add_group_to_user('handle_pro')
        self.client.force_authenticate(self.user)
        self.object = self.user.pro
        response = self.get_update_response(data={'company': 'New company'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_logged_in_content_returned(self):
        self.user = self.generate_user()
        self.add_group_to_user('handle_pro')
        self.client.force_authenticate(self.user)
        self.object = self.user.pro
        response = self.get_update_response(data={'company': 'New company'})
        self.object.refresh_from_db()
        serializer = self.get_serializer(self.object)
        self.assertEqual(response.data, serializer.data)

    def test_destroy_not_logged_in_status_code(self):
        self.object = self.generate_object()
        response = self.get_destroy_response()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_destroy_logged_in_no_perms_status_code(self):
        self.user = self.generate_user()
        self.client.force_authenticate(self.user)
        self.object = self.user.pro
        response = self.get_destroy_response()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_destroy_logged_in_has_perms_status_code(self):
        self.user = self.generate_user()
        self.add_group_to_user('handle_pro')
        self.client.force_authenticate(self.user)
        self.object = self.user.pro
        response = self.get_destroy_response()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_destroy_logged_in_is_active_pro(self):
        self.user = self.generate_user()
        self.add_group_to_user('handle_pro')
        self.client.force_authenticate(self.user)
        self.object = self.user.pro
        self.get_destroy_response()
        self.object.refresh_from_db()
        self.assertFalse(self.object.is_active)

    def test_destroy_logged_in_is_active_user(self):
        self.user = self.generate_user()
        self.add_group_to_user('handle_pro')
        self.client.force_authenticate(self.user)
        self.object = self.user.pro
        self.get_destroy_response()
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
