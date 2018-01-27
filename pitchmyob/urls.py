# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url(r'^api/', include([
        url(r'^', include('apps.applicant.urls')),
        url(r'^', include('apps.authentication.urls')),
        url(r'^', include('apps.candidacy.urls')),
        url(r'^', include('apps.data.urls')),
        url(r'^', include('apps.job.urls')),
        url(r'^', include('apps.pro.urls')),
        url(r'^', include('apps.notification.urls')),
        url(r'^', include('apps.message.urls')),
    ])),
    url(r'^admin/', admin.site.urls),
    url(r'^docs/', include('rest_framework_docs.urls')),
]
