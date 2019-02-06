#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Django
from django.test import TestCase, tag
from django.urls import reverse

# Current django project
from newsletter.models import Post
from newsletter.tests.utils import create_user


@tag('post', 'view', 'list', 'anonymous')
class TestPostListViewAsAnonymous(TestCase):
    """Tests ListView for Post."""

    @classmethod
    def setUpTestData(cls):
        cls.dict, cls.user = create_user()

    def tests_list_view_empty(self):
        """Tests."""
        r = self.client.get(reverse('newsletter:post-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['post_list']), 0)

    def tests_list_view_one_breakfast(self):
        """Tests."""
        Post.objects.create(author=self.user)

        r = self.client.get(reverse('newsletter:post-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['post_list']), 1)

    def tests_list_view_multiple_breakfasts(self):
        """Tests."""
        for i in range(0, 10):
            Post.objects.create(author=self.user)

        r = self.client.get(reverse('newsletter:post-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['post_list']), 10)


@tag('post', 'view', 'list', 'logged')
class TestPostListViewAsLogged(TestCase):
    """Tests ListView for Post.

    Note: there is at least one user active in this test. It is the one created in the setUp method.
    """

    @classmethod
    def setUpTestData(cls):
        """Create a user that will be able to log in."""
        cls.dict, cls.user = create_user()

    def tests_list_view_empty(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('newsletter:post-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['post_list']), 0)

    def tests_list_view_one_breakfast(self):
        """Tests."""
        Post.objects.create(author=self.user)

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('newsletter:post-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['post_list']), 1)

    def tests_list_view_multiple_breakfasts(self):
        """Tests."""
        for i in range(0, 10):
            Post.objects.create(author=self.user)

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('newsletter:post-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['post_list']), 10)


@tag('post', 'view', 'list', 'staff')
class TestPostListViewAsStaff(TestCase):
    """Tests ListView for Post."""

    @classmethod
    def setUpTestData(cls):
        """Create a user that will be able to log in."""
        cls.dict, cls.user = create_user(staff=True)

    def tests_list_view_empty(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('newsletter:post-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['post_list']), 0)

    def tests_list_view_one_breakfast(self):
        """Tests."""
        Post.objects.create(author=self.user)

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('newsletter:post-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['post_list']), 1)

    def tests_list_view_multiple_breakfasts(self):
        """Tests."""
        for i in range(0, 10):
            Post.objects.create(author=self.user)

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('newsletter:post-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['post_list']), 10)


@tag('post', 'view', 'list', 'superuser')
class TestPostListViewAsSuperuser(TestCase):
    """Tests ListView for Post."""

    @classmethod
    def setUpTestData(cls):
        """Create a user that will be able to log in."""
        cls.dict, cls.user = create_user(superuser=True)

    def tests_list_view_empty(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('newsletter:post-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['post_list']), 0)

    def tests_list_view_one_breakfast(self):
        """Tests."""
        Post.objects.create(author=self.user)

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('newsletter:post-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['post_list']), 1)

    def tests_list_view_multiple_breakfasts(self):
        """Tests."""
        for i in range(0, 10):
            Post.objects.create(author=self.user)

        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        r = self.client.get(reverse('newsletter:post-list'))

        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['post_list']), 10)
