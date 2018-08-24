#!/usr/bin/env python
# coding=utf-8

"""Tests for `dj-newsletter` models module."""

from dj_newsletter.models import Post, Comment

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from django.test import TestCase


class TestPostModel(TestCase):
    """Test post class model."""

    def setUp(self):
        """Setup function."""
        self.user = get_user_model().objects.create_user(username="username", password="password")
        self.dict = {
            'title': "My Title",
            'author': self.user,
            "text": "My text"
        }

    def test_string_representation(self):
        """Test the string representation of the post model."""
        s = Post.objects.create(**self.dict)
        self.assertEqual(str(s), self.dict['title'])
        self.assertEqual(str(s), s.title)

    def test_verbose_name(self):
        """Test the verbose name in singular."""
        self.assertEqual(str(Post._meta.verbose_name), "post")

    def test_verbose_name_plural(self):
        """Test the verbose name in plural."""
        self.assertEqual(str(Post._meta.verbose_name_plural), "posts")

    def test_empty_text_md(self):
        """Test the text_md function of post class."""
        s = Post.objects.create(title="My Title", author=self.user)
        self.assertEqual(len(s.text_md()), 0)

        s = Post.objects.create(title="My Title", author=self.user, text="# Toto")
        self.assertIn("<h1>", s.text_md())
        self.assertIn("</h1>", s.text_md())

        s = Post.objects.create(title="My Title", author=self.user, text="## Toto")
        self.assertIn("<h2>", s.text_md())
        self.assertIn("</h2>", s.text_md())

        s = Post.objects.create(title="My Title", author=self.user, text="Toto")
        self.assertIn("<p>", s.text_md())
        self.assertIn("</p>", s.text_md())

        s = Post.objects.create(title="My Title", author=self.user, text="*Toto*")
        self.assertIn("<em>", s.text_md())
        self.assertIn("</em>", s.text_md())

        s = Post.objects.create(title="My Title", author=self.user, text="**Toto**")
        self.assertIn("<strong>", s.text_md())
        self.assertIn("</strong>", s.text_md())


class TestCommentModel(TestCase):
    """Test comment class model."""

    def setUp(self):
        """Setup function."""
        self.user = get_user_model().objects.create_user(username="username", password="password")
        self.post = Post.objects.create(title="My Title", author=self.user, text="My text")

    def test_string_representation(self):
        """Test the string representation of the comment model."""
        s = Comment.objects.create(post=self.post, author=self.user, text="Hello World")
        self.assertEqual(str(s), "My Title - username (1)")

    def test_verbose_name(self):
        """Test the verbose name in singular."""
        self.assertEqual(str(Comment._meta.verbose_name), "comment")

    def test_verbose_name_plural(self):
        """Test the verbose name in plural."""
        self.assertEqual(str(Comment._meta.verbose_name_plural), "comments")
