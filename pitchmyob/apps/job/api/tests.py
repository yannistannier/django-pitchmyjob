# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from rest_framework import status

from apps.authentication.factories import UserProFactory
from apps.data.factories import ContractTypeFactory, ExperienceFactory, StudyLevelFactory
from apps.core.api import tests

from .serializers import JobSerializer
from ..factories import JobFactory
from ..models import Job


class JobAPITestCase(tests.RetrieveAPITestCaseMixin,
                     tests.CreateAPITestCaseMixin,
                     tests.UpdateAPITestCaseMixin,
                     tests.DestroyAPITestCaseMixin,
                     tests.BaseAPITestCase):
    base_name = 'job'
    factory_class = JobFactory
    user_factory_class = UserProFactory
    serializer_class = JobSerializer

    def get_create_data(self):
        contract_type = ContractTypeFactory()
        experience = ExperienceFactory()
        studylevel = StudyLevelFactory()
        return {
            'title': 'Job title',
            'salary': '45000',
            'starting_date': 'ASAP',
            'skills': ['Competence 1', 'Competence 2'],
            'description': 'Description',
            'contract_types': [contract_type.pk],
            'experiences': [experience.pk],
            'study_levels': [studylevel.pk],
            'is_active': True,
        }

    def test_retrieve_not_logged_in_status_code(self):
        self.object = self.generate_object()
        response = self.get_retrieve_response()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_logged_in_not_related_pro_status_code(self):
        self.user = self.generate_user()
        self.client.force_authenticate(self.user)
        self.object = self.generate_object()
        response = self.get_retrieve_response()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_logged_in_related_pro_status_code(self):
        self.user = self.generate_user()
        self.client.force_authenticate(self.user)
        self.object = self.generate_object(pro=self.user.pro)
        response = self.get_retrieve_response()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_logged_in_related_pro_content_returned(self):
        self.user = self.generate_user()
        self.client.force_authenticate(self.user)
        self.object = self.generate_object(pro=self.user.pro)
        serializer = self.get_serializer(self.object)
        response = self.get_retrieve_response()
        self.assertEqual(response.data, serializer.data)

    def test_create_not_logged_in_status_code(self):
        response = self.get_create_response(data=self.get_create_data())
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_logged_in_related_pro_status_code(self):
        self.user = self.generate_user()
        self.client.force_authenticate(self.user)
        response = self.get_create_response(data=self.get_create_data())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_logged_in_related_pro_content_returned(self):
        self.user = self.generate_user()
        self.client.force_authenticate(self.user)
        response = self.get_create_response(data=self.get_create_data())
        self.object = Job.objects.get(pk=response.data.get('id'))
        serializer = self.get_serializer(self.object)
        self.assertEqual(response.data, serializer.data)

    def test_create_logged_in_related_pro_available_now(self):
        self.user = self.generate_user()
        self.client.force_authenticate(self.user)
        response = self.get_create_response(data=self.get_create_data())
        self.object = Job.objects.get(pk=response.data.get('id'))
        response = self.get_retrieve_response()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_not_logged_in_status_code(self):
        self.object = self.generate_object()
        response = self.get_update_response(data={'title': 'New title'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_logged_in_not_related_pro_status_code(self):
        self.user = self.generate_user()
        self.client.force_authenticate(self.user)
        self.object = self.generate_object()
        response = self.get_update_response(data={'title': 'New title'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_logged_in_related_pro_status_code(self):
        self.user = self.generate_user()
        self.client.force_authenticate(self.user)
        self.object = self.generate_object(pro=self.user.pro)
        response = self.get_update_response(data={'title': 'New title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_logged_in_related_pro_content_returned(self):
        self.user = self.generate_user()
        self.client.force_authenticate(self.user)
        self.object = self.generate_object(pro=self.user.pro)
        response = self.get_update_response(data={'title': 'New title'})
        self.object.refresh_from_db()
        serializer = self.get_serializer(self.object)
        self.assertEqual(response.data, serializer.data)

    def test_destroy_not_logged_in_status_code(self):
        self.object = self.generate_object()
        response = self.get_destroy_response()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_destroy_logged_in_not_related_pro_status_code(self):
        self.user = self.generate_user()
        self.client.force_authenticate(self.user)
        self.object = self.generate_object()
        response = self.get_destroy_response()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_destroy_logged_in_related_pro_status_code(self):
        self.user = self.generate_user()
        self.client.force_authenticate(self.user)
        self.object = self.generate_object(pro=self.user.pro)
        response = self.get_destroy_response()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_destroy_logged_in_related_pro_is_active_job(self):
        self.user = self.generate_user()
        self.client.force_authenticate(self.user)
        self.object = self.generate_object(pro=self.user.pro)
        self.get_destroy_response()
        self.object.refresh_from_db()
        self.assertFalse(self.object.is_active)

    def test_destroy_logged_in_related_pro_not_available_anymore(self):
        self.user = self.generate_user()
        self.client.force_authenticate(self.user)
        self.object = self.generate_object(pro=self.user.pro)
        self.get_destroy_response()
        response = self.get_retrieve_response()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
