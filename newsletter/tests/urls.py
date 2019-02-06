# coding=utf-8

"""URLS file for testing."""

# Future
from __future__ import absolute_import, unicode_literals

# Django
from django.conf.urls import include
from django.urls import path

urlpatterns = [
    path('', include('newsletter.urls', namespace='newsletter')),
]
