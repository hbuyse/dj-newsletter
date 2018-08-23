# coding=utf-8

"""URLS file for testing."""

from __future__ import absolute_import, unicode_literals

from django.conf.urls import include
from django.urls import path


urlpatterns = [
    path('', include('dj_newsletter.urls', namespace='dj_newsletter')),
]
