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
class TestPostDateDetailViewAsAnonymous(TestCase):
    """Tests."""

    @classmethod
    def setUpTestData(cls):
        cls.dict, cls.user = create_user()
        cls.post = Post.objects.create(author=cls.user)

    def test_get(self):
        """Tests."""
        r = self.client.get(reverse('newsletter:post-detail-date', 
                            kwargs={
                                'pk': self.post.id,
                                'year': self.post.created.year,
                                'month': self.post.created.month,
                                'day': self.post.created.day
                            }))
        self.assertEqual(r.status_code, 200)


@tag('post', 'view', 'detail', 'logged')
class TestPostDateDetailViewAsLogged(TestCase):
    """Tests."""

    @classmethod
    def setUpTestData(cls):
        """Setup for al the following tests."""
        cls.dict, cls.user = create_user()
        cls.post = Post.objects.create(author=cls.user)

    def test_get(self):
        """Tests."""
        r = self.client.get(reverse('newsletter:post-detail-date', 
                            kwargs={
                                'pk': self.post.id,
                                'year': self.post.created.year,
                                'month': self.post.created.month,
                                'day': self.post.created.day
                            }))
        self.assertEqual(r.status_code, 200)


@tag('post', 'view', 'detail', 'staff')
class TestPostDateDetailViewAsStaff(TestCase):
    """Tests."""

    @classmethod
    def setUpTestData(cls):
        """Tests."""
        cls.dict, cls.user = create_user(staff=True)
        cls.post = Post.objects.create(author=cls.user)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('newsletter:post-detail-date', 
                            kwargs={
                                'pk': self.post.id,
                                'year': self.post.created.year,
                                'month': self.post.created.month,
                                'day': self.post.created.day
                            }))

        self.assertEqual(r.status_code, 200)


@tag('post', 'view', 'detail', 'superuser')
class TestPostDateDetailViewAsSuperuser(TestCase):
    """Tests."""

    @classmethod
    def setUpTestData(cls):
        """Tests."""
        cls.dict, cls.user = create_user(superuser=True)
        cls.post = Post.objects.create(author=cls.user)

    def test_get(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('newsletter:post-detail-date', 
                            kwargs={
                                'pk': self.post.id,
                                'year': self.post.created.year,
                                'month': self.post.created.month,
                                'day': self.post.created.day
                            }))

        self.assertEqual(r.status_code, 200)
