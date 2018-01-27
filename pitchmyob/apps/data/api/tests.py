# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from rest_framework import status

from apps.core.api import tests

from .serializers import (IndustrySerializer, EmployeeSerializer, ContractTypeSerializer, ExperienceSerializer,
                          StudyLevelSerializer)
from ..factories import IndustryFactory, EmployeeFactory, ContractTypeFactory, ExperienceFactory, StudyLevelFactory


class IndustryAPITestCase(tests.ListAPITestCaseMixin, tests.BaseAPITestCase):
    base_name = 'industry'
    factory_class = IndustryFactory
    serializer_class = IndustrySerializer

    def test_list_status_code(self):
        response = self.get_list_response()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_nb_data_returned(self):
        data = self.generate_objects()
        response = self.get_list_response()
        self.assertTrue(len(response.data) == len(data))

    def test_list_content_returned(self):
        data = self.generate_objects()
        response = self.get_list_response()
        serializer = self.get_serializer(data, many=True)

        is_identical = len(response.data) == len(serializer.data)
        if is_identical:
            for obj in response.data:
                if obj not in serializer.data:
                    is_identical = False
                    break
        self.assertTrue(is_identical)


class EmployeeAPITestCase(tests.ListAPITestCaseMixin, tests.BaseAPITestCase):
    base_name = 'employee'
    factory_class = EmployeeFactory
    serializer_class = EmployeeSerializer

    def test_list_status_code(self):
        response = self.get_list_response()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_nb_data_returned(self):
        data = self.generate_objects()
        response = self.get_list_response()
        self.assertTrue(len(response.data) == len(data))

    def test_list_content_returned(self):
        data = self.generate_objects()
        response = self.get_list_response()
        serializer = self.get_serializer(data, many=True)

        is_identical = len(response.data) == len(serializer.data)
        if is_identical:
            for obj in response.data:
                if obj not in serializer.data:
                    is_identical = False
                    break
        self.assertTrue(is_identical)


class ContractTypeAPITestCase(tests.ListAPITestCaseMixin, tests.BaseAPITestCase):
    base_name = 'contracttype'
    factory_class = ContractTypeFactory
    serializer_class = ContractTypeSerializer

    def test_list_status_code(self):
        response = self.get_list_response()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_nb_data_returned(self):
        data = self.generate_objects()
        response = self.get_list_response()
        self.assertTrue(len(response.data) == len(data))

    def test_list_content_returned(self):
        data = self.generate_objects()
        response = self.get_list_response()
        serializer = self.get_serializer(data, many=True)

        is_identical = len(response.data) == len(serializer.data)
        if is_identical:
            for obj in response.data:
                if obj not in serializer.data:
                    is_identical = False
                    break
        self.assertTrue(is_identical)


class ExperienceAPITestCase(tests.ListAPITestCaseMixin, tests.BaseAPITestCase):
    base_name = 'experience'
    factory_class = ExperienceFactory
    serializer_class = ExperienceSerializer

    def test_list_status_code(self):
        response = self.get_list_response()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_nb_data_returned(self):
        data = self.generate_objects()
        response = self.get_list_response()
        self.assertTrue(len(response.data) == len(data))

    def test_list_content_returned(self):
        data = self.generate_objects()
        response = self.get_list_response()
        serializer = self.get_serializer(data, many=True)

        is_identical = len(response.data) == len(serializer.data)
        if is_identical:
            for obj in response.data:
                if obj not in serializer.data:
                    is_identical = False
                    break
        self.assertTrue(is_identical)


class StudyLevelAPITestCase(tests.ListAPITestCaseMixin, tests.BaseAPITestCase):
    base_name = 'studylevel'
    factory_class = StudyLevelFactory
    serializer_class = StudyLevelSerializer

    def test_list_status_code(self):
        response = self.get_list_response()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_nb_data_returned(self):
        data = self.generate_objects()
        response = self.get_list_response()
        self.assertTrue(len(response.data) == len(data))

    def test_list_content_returned(self):
        data = self.generate_objects()
        response = self.get_list_response()
        serializer = self.get_serializer(data, many=True)

        is_identical = len(response.data) == len(serializer.data)
        if is_identical:
            for obj in response.data:
                if obj not in serializer.data:
                    is_identical = False
                    break
        self.assertTrue(is_identical)
