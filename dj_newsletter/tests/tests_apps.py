#!/usr/bin/env python
# coding=utf-8

"""
test_dj-sponsoring
------------

Tests for `dj-sponsoring` apps module.
"""

from dj_newsletter.apps import DjNewsletterConfig

from django.apps import apps
from django.test import TestCase


class TestApps(TestCase):

    def test_apps(self):
        self.assertEqual(DjNewsletterConfig.name, 'dj_newsletter')
        self.assertEqual(apps.get_app_config('dj_newsletter').name, 'dj_newsletter')
