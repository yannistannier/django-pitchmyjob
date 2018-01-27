# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import json
import os
import uuid

import boto3

from django.conf import settings

from apps.authentication.models import User


def generate_upload_to(instance, filename):
    directory = str(instance.__class__.__name__.lower())
    filename, extension = os.path.splittext(filename)
    filename = str(uuid.uuid4()) + str(extension)
    return '{}/{}/{}'.format(directory, instance.id, filename)


class Email(object):
    def __init__(self, subject, to, context=None, template='default.html', from_email=None, reply_to=None, secure=1):
        self.subject = subject
        self.template = template
        self.context = context or {}
        self.from_email = from_email or settings.DEFAULT_FROM_EMAIL
        self.reply_to = reply_to or self.from_email
        self.secure = secure

        if isinstance(to, User):
            self.to = [to.email]
        elif isinstance(to, str):
            self.to = [to]
        elif isinstance(to, list):
            self.to = to

    def send(self, force=False):
        message = json.dumps({
            'uuid': str(uuid.uuid4()),
            'subject': self.subject,
            'to': self.to,
            'from_email': self.from_email,
            'reply_to': self.reply_to,
            'template': self.template,
            'context': self.context,
            'secure': self.secure,
        })

        if settings.DEBUG or force:
            sns = boto3.client('sns')
            sns.publish(
                TopicArn=settings.SNS_EMAIL,
                Message=message,
                MessageStructure='string'
            )
        else:
            sqs = boto3.resource('sqs')
            queue = sqs.get_queue_by_name(QueueName=settings.SQS_EMAIL)
            queue.send_message(MessageBody=message)
