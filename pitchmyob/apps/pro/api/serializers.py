# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from apps.authentication.api.serializers import UserRegisterSerializer
from apps.authentication.models import User

from ..models import Pro


class ProSerializer(serializers.ModelSerializer):
    logo = Base64ImageField(required=False, default=Pro.DEFAULT_LOGO)

    class Meta:
        model = Pro
        exclude = ('is_active', )


class UserRegisterCollaboratorSerializer(UserRegisterSerializer):
    photo = Base64ImageField(required=False, default=User.DEFAULT_PHOTO)

    class Meta(UserRegisterSerializer.Meta):
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'photo')

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['pro'] = request.user.pro
        return super(UserRegisterCollaboratorSerializer, self).create(validated_data)
