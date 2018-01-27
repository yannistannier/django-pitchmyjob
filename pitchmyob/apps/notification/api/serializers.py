# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from rest_framework import serializers

from apps.authentication.api.serializers import UserSerializer
from apps.authentication.models import User
from apps.job.api.serializers import JobSerializer
from apps.job.models import Job

from ..models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    emmiter = UserSerializer(read_only=True)
    action_object = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ('id', 'type_name', 'emmiter', 'action_object', 'created', 'is_unread')
        read_only_fields = ('id', 'type_name', 'emmiter', 'action_object', 'created')

    def get_action_object(self, obj):
        action_object = obj.action_object

        if isinstance(action_object, User):
            serializer = UserSerializer(action_object)
        elif isinstance(action_object, Job):
            serializer = JobSerializer(action_object)
        else:
            raise Exception('Unexpected type action_object')
        return serializer.data
