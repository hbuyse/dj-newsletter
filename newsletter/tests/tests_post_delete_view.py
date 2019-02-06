#! /usr/bin/env python
# coding=utf-8

"""Tests the modification view of a post."""

# Django
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase, override_settings, tag
from django.urls import reverse

# Current django project
from newsletter.models import Post
from newsletter.tests.utils import create_user


@override_settings(LOGIN_URL="/toto/")
@tag('post', 'view', 'delete', 'anonymous')
class TestPostUpdateViewAsAnonymous(TestCase):
    """Tests the modification view of a post as an anonymous user."""

    @classmethod
    def setUpTestData(cls):
        """Set up for all the following tests."""
        cls.dict, cls.user = create_user()
        d = {
            'author': cls.user,
            'text': 'Text',
            'title': 'Title'
        }
        cls.post = Post.objects.create(**d)

    def test_get_redirected_to_login(self):
        """Get should be redirected to the login page."""
        response = self.client.get(reverse('newsletter:post-delete', kwargs={'pk': self.post.id}))

        self.assertRedirects(response, "/toto/?next=/{}/delete/".format(self.post.id), fetch_redirect_response=False)

    def test_post_redirected_to_login(self):
        """Post should be redirected to the login page."""
        d = {
            'title': 'My title'
        }
        response = self.client.post(reverse('newsletter:post-delete', kwargs={'pk': self.post.id}))

        self.assertRedirects(response, "/toto/?next=/{}/delete/".format(self.post.id), fetch_redirect_response=False)


@tag('post', 'view', 'delete', 'logged')
class TestPostUpdateViewAsLogged(TestCase):
    """Tests."""

    @classmethod
    def setUpTestData(cls):
        """Set up for all the following tests."""
        cls.dict, cls.user = create_user()
        d = {
            'author': cls.user,
            'text': 'Text',
            'title': 'Title'
        }
        cls.post = Post.objects.create(**d)

    def test_posts_create_view_get_as_logged_with_wrong_permissions(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))

        response = self.client.get(reverse('newsletter:post-delete', kwargs={'pk': self.post.id}))
        self.assertEqual(response.status_code, 403)

    def test_posts_create_view_post_as_logged_with_wrong_permissions(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))

        response = self.client.post(reverse('newsletter:post-delete', kwargs={'pk': self.post.id}))
        self.assertEqual(response.status_code, 403)

    def test_posts_create_view_get_as_logged_with_right_permissions(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        self.assertFalse(self.user.has_perm('newsletter.delete_post'))

        self.user.user_permissions.add(Permission.objects.get(name='Can delete post'))
        response = self.client.get(reverse('newsletter:post-delete', kwargs={'pk': self.post.id}))
        self.assertEqual(response.status_code, 200)

    def test_posts_create_view_post_as_logged_with_right_permissions(self):
        """Tests."""
        perms = 'newsletter.delete_post'
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        self.assertFalse(self.user.has_perm(perms))
        self.user.user_permissions.add(Permission.objects.get(codename=perms.split('.')[1]))

        # Permission caching (https://docs.djangoproject.com/en/2.1/topics/auth/default/#permission-caching)
        # Need to refetch the user to get the new permissions
        self.user = get_user_model().objects.get(id=self.user.id)
        self.assertTrue(self.user.has_perm(perms))

        # Next test
        self.assertEqual(len(Post.objects.all()), 1)
        response = self.client.post(reverse('newsletter:post-delete', kwargs={'pk': self.post.id}))
        self.assertEqual(len(Post.objects.all()), 0)
        self.assertRedirects(response, "/", fetch_redirect_response=False)


@tag('post', 'view', 'delete', 'staff')
class TestPostUpdateViewAsStaff(TestCase):
    """Tests."""

    @classmethod
    def setUpTestData(cls):
        """Set up for all the following tests."""
        cls.dict, cls.user = create_user(staff=True)
        d = {
            'author': cls.user,
            'text': 'Text',
            'title': 'Title'
        }
        cls.post = Post.objects.create(**d)

    def test_posts_create_view_get_as_logged_with_wrong_permissions(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))

        response = self.client.get(reverse('newsletter:post-delete', kwargs={'pk': self.post.id}))
        self.assertEqual(response.status_code, 403)

    def test_posts_create_view_post_as_logged_with_wrong_permissions(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))

        response = self.client.post(reverse('newsletter:post-delete', kwargs={'pk': self.post.id}))
        self.assertEqual(response.status_code, 403)

    def test_posts_create_view_get_as_logged_with_right_permissions(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        self.assertFalse(self.user.has_perm('newsletter.delete_post'))

        self.user.user_permissions.add(Permission.objects.get(name='Can delete post'))
        response = self.client.get(reverse('newsletter:post-delete', kwargs={'pk': self.post.id}))
        self.assertEqual(response.status_code, 200)

    def test_posts_create_view_post_as_logged_with_right_permissions(self):
        """Tests."""
        perms = 'newsletter.delete_post'
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        self.assertFalse(self.user.has_perm(perms))
        self.user.user_permissions.add(Permission.objects.get(codename=perms.split('.')[1]))

        # Permission caching (https://docs.djangoproject.com/en/2.1/topics/auth/default/#permission-caching)
        # Need to refetch the user to get the new permissions
        self.user = get_user_model().objects.get(id=self.user.id)
        self.assertTrue(self.user.has_perm(perms))

        # Next test
        self.assertEqual(len(Post.objects.all()), 1)
        response = self.client.post(reverse('newsletter:post-delete', kwargs={'pk': self.post.id}))
        self.assertEqual(len(Post.objects.all()), 0)
        self.assertRedirects(response, "/", fetch_redirect_response=False)


@tag('post', 'view', 'delete', 'superuser')
class TestPostUpdateViewAsSuperuser(TestCase):
    """Tests the modification of a post as superuser.
    
    Unlike simple user or staff user, superuser already has the rights to do whatever he/she wants.
    """

    @classmethod
    def setUpTestData(cls):
        """Set up for all the following tests."""
        cls.dict, cls.user = create_user(superuser=True)
        d = {
            'author': cls.user,
            'text': 'Text',
            'title': 'Title'
        }
        cls.post = Post.objects.create(**d)

    def test_posts_create_view_get_as_logged_with_right_permissions(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        self.assertTrue(self.user.has_perm('newsletter.delete_post'))

        response = self.client.get(reverse('newsletter:post-delete', kwargs={'pk': self.post.id}))
        self.assertEqual(response.status_code, 200)

    def test_posts_create_view_post_as_logged_with_right_permissions(self):
        """Tests."""
        perms = 'newsletter.delete_post'
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        self.assertTrue(self.user.has_perm(perms))

        # Next test
        self.assertEqual(len(Post.objects.all()), 1)
        response = self.client.post(reverse('newsletter:post-delete', kwargs={'pk': self.post.id}))
        self.assertEqual(len(Post.objects.all()), 0)
        self.assertRedirects(response, "/", fetch_redirect_response=False)
