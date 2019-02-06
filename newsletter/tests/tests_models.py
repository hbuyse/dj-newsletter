#!/usr/bin/env python
# coding=utf-8

"""Tests for `newsletter` models module."""

# Django
from django.contrib.auth import get_user_model
from django.test import TestCase

# Current django project
from newsletter.models import Comment, Post


class TestPostModel(TestCase):
    """Test post class model."""

    def setUp(self):
        """Set up function."""
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

    def test_text_md(self):
        """Test the text_md function of post class."""
        s = Post.objects.create(title="My Title", author=self.user)
        self.assertEqual(len(s.text_md()), 0)

        tests = (
            ("# Toto", "<h1>", "</h1>"),
            ("## Toto", "<h2>", "</h2>"),
            ("Toto", "<p>", "</p>"),
            ("*Toto*", "<em>", "</em>"),
            ("**Toto**", "<strong>", "</strong>"),
        )

        for test in tests:
            p = Post.objects.create(title="My Title", author=self.user, text=test[0])
            self.assertIn(test[1], p.text_md())
            self.assertIn(test[2], p.text_md())


class TestCommentModel(TestCase):
    """Test comment class model."""

    def setUp(self):
        """Set up function."""
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
