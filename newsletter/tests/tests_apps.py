#!/usr/bin/env python
# coding=utf-8

"""Tests for `newsletter` apps module."""

# Django
from django.apps import apps
from django.test import TestCase

# Current django project
from newsletter.apps import NewsletterConfig


class TestApps(TestCase):

    def test_apps(self):
        self.assertEqual(NewsletterConfig.name, 'newsletter')
        self.assertEqual(apps.get_app_config('newsletter').name, 'newsletter')
