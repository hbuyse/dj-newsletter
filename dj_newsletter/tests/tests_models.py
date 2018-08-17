#!/usr/bin/env python
# coding=utf-8

"""
test_dj-newsletter
------------

Tests for `dj-newsletter` models module.
"""

from dj_newsletter.models import Post

from django.contrib.auth.models import User
from django.test import TestCase


class TestPostModel(TestCase):

    def setUp(self):
        """Tests."""
        self.user = User.objects.create_user(username="username", password="password")
        self.dict = {
            'title': "My Title",
            'author' : self.user,
            "text": "My text"
        }

    def test_string_representation(self):
        s = Post(**self.dict)
        self.assertEqual(str(s), self.dict['title'])
        self.assertEqual(str(s), s.title)

    def test_verbose_name(self):
        self.assertEqual(str(Post._meta.verbose_name), "post")

    def test_verbose_name_plural(self):
        self.assertEqual(str(Post._meta.verbose_name_plural), "posts")

    def test_empty_text_md(self):
        s = Post()
        self.assertEqual(len(s.text_md()), 0)
        self.assertNotIn("<h1>", s.text_md())

    def test_text_md(self):
        s = Post(text="# Toto")
        self.assertIn("<h1>", s.text_md())
        self.assertIn("</h1>", s.text_md())

        s = Post(text="## Toto")
        self.assertIn("<h2>", s.text_md())
        self.assertIn("</h2>", s.text_md())

        s = Post(text="Toto")
        self.assertIn("<p>", s.text_md())
        self.assertIn("</p>", s.text_md())

        s = Post(text="*Toto*")
        self.assertIn("<em>", s.text_md())
        self.assertIn("</em>", s.text_md())

        s = Post(text="**Toto**")
        self.assertIn("<strong>", s.text_md())
        self.assertIn("</strong>", s.text_md())
