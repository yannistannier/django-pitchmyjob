# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import uuid

import boto3

from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from django.utils.translation import ugettext as _

from apps.applicant.models import Applicant
from apps.core.utils import Email
from apps.pro.models import Pro

from ..models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    token = serializers.CharField(source='auth_token.key', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'token']
        read_only_fields = ('id',)
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def create(self, validated_data):
        is_active = not settings.REGISTER_CONFIRMATION
        token = str(uuid.uuid4())
        validated_data['confirm_email_token'] = token
        validated_data['confirm_phone_token'] = token[:6]
        return User.objects.create_user(username=validated_data['email'], is_active=is_active, **validated_data)


class UserRegisterApplicantSerializer(UserRegisterSerializer):
    photo = Base64ImageField(required=False, default=User.DEFAULT_PHOTO)

    class Meta(UserRegisterSerializer.Meta):
        fields = UserRegisterSerializer.Meta.fields + ['photo']

    def create(self, validated_data):
        photo = validated_data.pop('photo', None)
        user = super(UserRegisterApplicantSerializer, self).create(validated_data)
        user.photo = photo
        user.save()
        Applicant.objects.create(user=user)

        if settings.REGISTER_CONFIRMATION:
            client = boto3.client('sns')
            phone_token = validated_data.get('confirm_phone_token')
            msg = 'Saisissez le code {} pour confirmer votre inscription sur Spitch.com'.format(phone_token)
            client.publish(Message=msg, PhoneNumber=user.phone)
        return user


class UserRegisterProSerializer(UserRegisterSerializer):
    company = serializers.CharField(source='pro.company')

    class Meta(UserRegisterSerializer.Meta):
        fields = UserRegisterSerializer.Meta.fields + ['company', 'position', 'phone']

    def create(self, validated_data):
        pro = Pro.objects.create(company=validated_data['pro']['company'])
        validated_data['pro'] = pro
        user = super(UserRegisterProSerializer, self).create(validated_data)
        user.groups.add(Group.objects.get(name='handle_pro'))
        user.groups.add(Group.objects.get(name='handle_collaborator'))

        if settings.REGISTER_CONFIRMATION:
            context = {
                'name': user.get_full_name(),
                'token': user.confirm_email_token,
            }
            Email(subject='Confirmation d\'inscription', to=user, context=context,
                  template='pro/register_confirm.html').send()
        return user


class AutLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        login_type = self.context.get('login_type')

        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(email=email, password=password)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg, code='authorization')
                elif login_type == 'applicant' and not hasattr(user, 'applicant'):
                    msg = _('User account isn\'t linked to a applicant')
                    raise serializers.ValidationError(msg, code='authorization')
                elif login_type == 'pro' and not user.pro:
                    msg = _('User account isn\'t linked to a company')
                    raise serializers.ValidationError(msg, code='authorization')
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=False, default=User.DEFAULT_PHOTO)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'photo', 'is_pro', 'is_applicant')
        read_only_fields = ('id', 'email', 'is_pro', 'is_applicant')


class ForgetPasswordRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)

    def update(self, instance, validated_data):
        instance.lost_password_token = str(uuid.uuid4())
        instance.save()
        return instance


class ForgetPasswordConfirmSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password',)
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def update(self, instance, validated_data):
        instance.lost_password_token = ''
        instance.set_password(validated_data.get('password'))
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('old_password', 'new_password')

    def validate_old_password(self, value):
        request = self.context.get('request')
        if not request.user.check_password(value):
            raise serializers.ValidationError(_('L\'ancien mot de passe n\'est pas valide'))
        return value

    def update(self, instance, validated_data):
        instance.lost_password_token = ''
        instance.set_password(validated_data.get('new_password'))
        instance.save()
        return instance


class UserRegisterConfirmSerializer(serializers.ModelSerializer):
    token_field = None

    class Meta:
        model = User
        fields = ('email',)

    def update(self, instance, validated_data):
        setattr(instance, self.token_field, '')
        setattr(instance, 'is_active', True)
        instance.save()
        return instance


class UserRegisterConfirmApplicantSerializer(UserRegisterConfirmSerializer):
    token_field = 'confirm_phone_token'


class UserRegisterConfirmProSerializer(UserRegisterConfirmSerializer):
    token_field = 'confirm_email_token'
