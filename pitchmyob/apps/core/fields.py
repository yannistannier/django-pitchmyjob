# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import os
import uuid

from django.db import models


class ImageField(models.ImageField):
    def generate_filename(self, instance, filename):
        model_name = str(instance.__class__.__name__.lower())
        model_field_name = str(self.name)
        filename, extension = os.path.splitext(filename)
        filename = str(uuid.uuid4()) + str(extension).lower()
        return '{}/{}/{}/{}'.format(model_name, instance.id, model_field_name, filename)
