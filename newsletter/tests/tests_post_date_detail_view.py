#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Django
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
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
        """Setup for al the following tests."""
        cls.author_dict, cls.author = create_user()
        cls.post = Post.objects.create(author=cls.author)

    def test_get(self):
        """Tests."""
        response = self.client.get(reverse('newsletter:post-detail-date',
                                           kwargs={
                                               'year': self.post.created.year,
                                               'month': self.post.created.month,
                                               'day': self.post.created.day,
                                               'pk': self.post.id
                                           }))
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        """Tests."""
        d = {
            'text': 'Text'
        }
        response = self.client.post(reverse('newsletter:post-detail-date',
                                            kwargs={
                                                'year': self.post.created.year,
                                                'month': self.post.created.month,
                                                'day': self.post.created.day,
                                                'pk': self.post.id
                                            }), d)
        self.assertEqual(response.status_code, 403)


@tag('post', 'view', 'detail', 'logged')
class TestPostDetailViewAsLogged(TestCase):
    """Tests."""

    @classmethod
    def setUpTestData(cls):
        """Setup for al the following tests."""
        cls.dict, cls.user = create_user()
        cls.post = Post.objects.create(author=cls.user)
        cls.perms = 'newsletter.add_comment'

    def test_get_with_wrong_permissions(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))

        response = self.client.get(reverse('newsletter:post-detail-date',
                                           kwargs={
                                               'year': self.post.created.year,
                                               'month': self.post.created.month,
                                               'day': self.post.created.day,
                                               'pk': self.post.id
                                           }))
        self.assertEqual(response.status_code, 200)

    def test_post_with_wrong_permissions(self):
        """Tests."""
        d = {
            'text': 'Text'
        }
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))

        response = self.client.post(reverse('newsletter:post-detail-date',
                                            kwargs={
                                                'year': self.post.created.year,
                                                'month': self.post.created.month,
                                                'day': self.post.created.day,
                                                'pk': self.post.id
                                            }), d)
        self.assertEqual(response.status_code, 403)

    def test_get_with_right_permissions(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        self.assertFalse(self.user.has_perm(self.perms))
        self.user.user_permissions.add(Permission.objects.get(codename=self.perms.split('.')[1]))

        response = self.client.get(reverse('newsletter:post-detail-date',
                                           kwargs={
                                               'year': self.post.created.year,
                                               'month': self.post.created.month,
                                               'day': self.post.created.day,
                                               'pk': self.post.id
                                           }))
        self.assertEqual(response.status_code, 200)

    def test_post_with_right_permissions_but_empty_text(self):
        """Tests."""
        d = {
            'text': ''
        }
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        self.assertFalse(self.user.has_perm(self.perms))
        self.user.user_permissions.add(Permission.objects.get(codename=self.perms.split('.')[1]))

        # Permission caching (https://docs.djangoproject.com/en/2.1/topics/auth/default/#permission-caching)
        # Need to refetch the user to get the new permissions
        self.user = get_user_model().objects.get(id=self.user.id)
        self.assertTrue(self.user.has_perm(self.perms))

        # Next test
        response = self.client.post(reverse('newsletter:post-detail-date',
                                            kwargs={
                                                'year': self.post.created.year,
                                                'month': self.post.created.month,
                                                'day': self.post.created.day,
                                                'pk': self.post.id
                                            }), data=d)
        self.assertEqual(len(Post.objects.all()), 1)
        self.assertFormError(response, 'form', 'text', "This field is required.")

    def test_post_with_right_permissions(self):
        """Tests."""
        d = {
            'text': 'Text'
        }
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        self.assertFalse(self.user.has_perm(self.perms))
        self.user.user_permissions.add(Permission.objects.get(codename=self.perms.split('.')[1]))

        # Permission caching (https://docs.djangoproject.com/en/2.1/topics/auth/default/#permission-caching)
        # Need to refetch the user to get the new permissions
        self.user = get_user_model().objects.get(id=self.user.id)
        self.assertTrue(self.user.has_perm(self.perms))

        # Next test
        response = self.client.post(reverse('newsletter:post-detail-date',
                                            kwargs={
                                                'year': self.post.created.year,
                                                'month': self.post.created.month,
                                                'day': self.post.created.day,
                                                'pk': self.post.id
                                            }), data=d)
        self.assertEqual(len(Post.objects.all()), 1)
        self.assertRedirects(response, "/{}/{}/{}/{}/".format(self.post.created.year, self.post.created.month, self.post.created.day, self.post.id), fetch_redirect_response=False)


@tag('post', 'view', 'detail', 'staff')
class TestPostDetailViewAsStaff(TestCase):
    """Tests."""

    @classmethod
    def setUpTestData(cls):
        """Tests."""
        cls.dict, cls.user = create_user(staff=True)
        cls.post = Post.objects.create(author=cls.user)
        cls.perms = 'newsletter.add_comment'

    def test_get_with_wrong_permissions(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))

        response = self.client.get(reverse('newsletter:post-detail-date',
                                           kwargs={
                                               'year': self.post.created.year,
                                               'month': self.post.created.month,
                                               'day': self.post.created.day,
                                               'pk': self.post.id
                                           }))
        self.assertEqual(response.status_code, 200)

    def test_post_with_wrong_permissions(self):
        """Tests."""
        d = {
            'text': 'Text'
        }
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))

        response = self.client.post(reverse('newsletter:post-detail-date',
                                            kwargs={
                                                'year': self.post.created.year,
                                                'month': self.post.created.month,
                                                'day': self.post.created.day,
                                                'pk': self.post.id
                                            }), d)
        self.assertEqual(response.status_code, 403)

    def test_get_with_right_permissions(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        self.assertFalse(self.user.has_perm(self.perms))
        self.user.user_permissions.add(Permission.objects.get(codename=self.perms.split('.')[1]))

        response = self.client.get(reverse('newsletter:post-detail-date',
                                           kwargs={
                                               'year': self.post.created.year,
                                               'month': self.post.created.month,
                                               'day': self.post.created.day,
                                               'pk': self.post.id
                                           }))
        self.assertEqual(response.status_code, 200)

    def test_post_with_right_permissions_but_empty_text(self):
        """Tests."""
        d = {
            'text': ''
        }
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        self.assertFalse(self.user.has_perm(self.perms))
        self.user.user_permissions.add(Permission.objects.get(codename=self.perms.split('.')[1]))

        # Permission caching (https://docs.djangoproject.com/en/2.1/topics/auth/default/#permission-caching)
        # Need to refetch the user to get the new permissions
        self.user = get_user_model().objects.get(id=self.user.id)
        self.assertTrue(self.user.has_perm(self.perms))

        # Next test
        response = self.client.post(reverse('newsletter:post-detail-date',
                                            kwargs={
                                                'year': self.post.created.year,
                                                'month': self.post.created.month,
                                                'day': self.post.created.day,
                                                'pk': self.post.id
                                            }), data=d)
        self.assertEqual(len(Post.objects.all()), 1)
        self.assertFormError(response, 'form', 'text', "This field is required.")

    def test_post_with_right_permissions(self):
        """Tests."""
        d = {
            'text': 'Text'
        }
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        self.assertFalse(self.user.has_perm(self.perms))
        self.user.user_permissions.add(Permission.objects.get(codename=self.perms.split('.')[1]))

        # Permission caching (https://docs.djangoproject.com/en/2.1/topics/auth/default/#permission-caching)
        # Need to refetch the user to get the new permissions
        self.user = get_user_model().objects.get(id=self.user.id)
        self.assertTrue(self.user.has_perm(self.perms))

        # Next test
        response = self.client.post(reverse('newsletter:post-detail-date',
                                            kwargs={
                                                'year': self.post.created.year,
                                                'month': self.post.created.month,
                                                'day': self.post.created.day,
                                                'pk': self.post.id
                                            }), data=d)
        self.assertEqual(len(Post.objects.all()), 1)
        self.assertRedirects(response, "/{}/{}/{}/{}/".format(self.post.created.year, self.post.created.month, self.post.created.day, self.post.id), fetch_redirect_response=False)


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

        response = self.client.get(reverse('newsletter:post-detail-date',
                                           kwargs={
                                               'year': self.post.created.year,
                                               'month': self.post.created.month,
                                               'day': self.post.created.day,
                                               'pk': self.post.id
                                           }))
        self.assertEqual(response.status_code, 200)

    def test_post_but_empty_text(self):
        """Tests."""
        d = {
            'text': ''
        }
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))

        response = self.client.post(reverse('newsletter:post-detail-date',
                                            kwargs={
                                                'year': self.post.created.year,
                                                'month': self.post.created.month,
                                                'day': self.post.created.day,
                                                'pk': self.post.id
                                            }), data=d)
        self.assertEqual(len(Post.objects.all()), 1)
        self.assertFormError(response, 'form', 'text', "This field is required.")

    def test_post(self):
        """Tests."""
        d = {
            'text': 'Text'
        }
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))

        response = self.client.post(reverse('newsletter:post-detail-date',
                                            kwargs={
                                                'year': self.post.created.year,
                                                'month': self.post.created.month,
                                                'day': self.post.created.day,
                                                'pk': self.post.id
                                            }), data=d)
        self.assertEqual(len(Post.objects.all()), 1)
        self.assertRedirects(response, "/{}/{}/{}/{}/".format(self.post.created.year, self.post.created.month, self.post.created.day, self.post.id), fetch_redirect_response=False)
