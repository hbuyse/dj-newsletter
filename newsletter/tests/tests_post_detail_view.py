#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Django
from django.test import TestCase, tag
from django.urls import reverse

# Current django project
from newsletter.models import Post
from newsletter.tests.utils import create_user


@tag('post', 'view', 'detail', 'anonymous')
class TestPostDetailViewAsAnonymous(TestCase):
    """Tests."""

    @classmethod
    def setUpTestData(cls):
        cls.author_dict, cls.author = create_user()
        cls.post = Post.objects.create(author=cls.author)

    def test_get(self):
        """Tests."""
        r = self.client.get(reverse('newsletter:post-detail', kwargs={'pk': self.post.id}))
        self.assertEqual(r.status_code, 200)


@tag('post', 'view', 'detail', 'logged')
class TestPostDetailViewAsLogged(TestCase):
    """Tests."""

    @classmethod
    def setUpTestData(cls):
        """Setup for al the following tests."""
        cls.dict, cls.user = create_user()
        cls.post = Post.objects.create(author=cls.user)

    def test_get(self):
        """Tests."""
        r = self.client.get(reverse('newsletter:post-detail', kwargs={'pk': self.post.id}))
        self.assertEqual(r.status_code, 200)


@tag('post', 'view', 'detail', 'staff')
class TestPostDetailViewAsStaff(TestCase):
    """Tests."""

    @classmethod
    def setUpTestData(cls):
        """Tests."""
        cls.dict, cls.user = create_user(staff=True)
        cls.post = Post.objects.create(author=cls.user)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('newsletter:post-detail', kwargs={'pk': self.post.id}))

        self.assertEqual(r.status_code, 200)


@tag('post', 'view', 'detail', 'superuser')
class TestPostDetailViewAsSuperuser(TestCase):
    """Tests."""

    @classmethod
    def setUpTestData(cls):
        """Tests."""
        cls.dict, cls.user = create_user(superuser=True)
        cls.post = Post.objects.create(author=cls.user)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('newsletter:post-detail', kwargs={'pk': self.post.id}))

        self.assertEqual(r.status_code, 200)
