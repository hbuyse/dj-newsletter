#! /usr/bin/env python
# coding=utf-8

"""Tests the modification view of a self.post."""

# Django
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase, override_settings, tag
from django.urls import reverse

# Current django project
from newsletter.models import Comment, Post
from newsletter.tests.helper import UserHelper


@override_settings(LOGIN_URL="/toto/")
@tag('comment', 'view', 'delete', 'anonymous')
class TestCommentDeleteViewAsAnonymous(TestCase):
    """Tests the modification view of a post as an anonymous user."""

    @classmethod
    def setUpTestData(cls):
        """Set up for all the following tests."""
        cls.author = UserHelper()
        d = {
            'author': cls.author,
            'text': 'Text',
            'title': 'Title'
        }
        cls.post = Post.objects.create(**d)
        cls.comment = Comment.objects.create(post=cls.post, text="Hello World", author=cls.author)

    def test_get_redirected_to_login(self):
        """Get should be redirected to the login page."""
        response = self.client.get(reverse('newsletter:post-comment-delete', kwargs={'pk': self.post.id}))
        self.assertRedirects(response, "/toto/?next=/comments/{}/delete/".format(self.comment.id), fetch_redirect_response=False)

    def test_post_redirected_to_login(self):
        """Post should be redirected to the login page."""
        d = {
            'title': 'My title'
        }
        response = self.client.post(reverse('newsletter:post-comment-delete', kwargs={'pk': self.post.id}))
        self.assertRedirects(response, "/toto/?next=/comments/{}/delete/".format(self.comment.id), fetch_redirect_response=False)


@tag('comment', 'view', 'delete', 'logged')
class TestCommentDeleteViewAsLogged(TestCase):
    """Tests."""

    @classmethod
    def setUpTestData(cls):
        """Set up for all the following tests."""
        cls.dict, cls.user = UserHelper()
        d = {
            'author': cls.user,
            'text': 'Text',
            'title': 'Title'
        }
        cls.post = Post.objects.create(**d)
        cls.comment = Comment.objects.create(post=cls.post, text="Hello World", author=cls.user)
    
    def setUp(self):
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))

    def test_get_as_logged_with_wrong_permissions(self):
        """Tests."""

        response = self.client.get(reverse('newsletter:post-comment-delete', kwargs={'pk': self.post.id}))
        self.assertEqual(response.status_code, 403)

    def test_post_as_logged_with_wrong_permissions(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))

        response = self.client.post(reverse('newsletter:post-comment-delete', kwargs={'pk': self.post.id}))
        self.assertEqual(response.status_code, 403)

    def test_get_as_logged_with_right_permissions(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        self.assertFalse(self.user.has_perm('newsletter.delete_comment'))

        self.user.user_permissions.add(Permission.objects.get(name='Can delete comment'))
        response = self.client.get(reverse('newsletter:post-comment-delete', kwargs={'pk': self.post.id}))
        self.assertEqual(response.status_code, 200)

    def test_post_as_logged_with_right_permissions(self):
        """Tests."""
        perms = 'newsletter.delete_comment'
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        self.assertFalse(self.user.has_perm(perms))
        self.user.user_permissions.add(Permission.objects.get(codename=perms.split('.')[1]))

        # Permission caching (https://docs.djangoproject.com/en/2.1/topics/auth/default/#permission-caching)
        # Need to refetch the user to get the new permissions
        self.user = get_user_model().objects.get(id=self.user.id)
        self.assertTrue(self.user.has_perm(perms))

        # Next test
        response = self.client.post(reverse('newsletter:post-comment-delete', kwargs={'pk': self.post.id}))
        self.assertEqual(len(Post.objects.all()), 1)
        self.assertRedirects(response, "/{}/{}/{}/{}/".format(self.post.created.year, self.post.created.month, self.post.created.day, self.post.id), fetch_redirect_response=False)


@tag('comment', 'view', 'delete', 'staff')
class TestCommentDeleteViewAsStaff(TestCase):
    """Tests."""

    @classmethod
    def setUpTestData(cls):
        """Set up for all the following tests."""
        cls.dict, cls.user = UserHelper(staff=True)
        d = {
            'author': cls.user,
            'text': 'Text',
            'title': 'Title'
        }
        cls.post = Post.objects.create(**d)
        cls.comment = Comment.objects.create(post=cls.post, text="Hello World", author=cls.user)

    def test_get_as_logged_with_wrong_permissions(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))

        response = self.client.get(reverse('newsletter:post-comment-delete', kwargs={'pk': self.post.id}))
        self.assertEqual(response.status_code, 403)

    def test_post_as_logged_with_wrong_permissions(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))

        response = self.client.post(reverse('newsletter:post-comment-delete', kwargs={'pk': self.post.id}))
        self.assertEqual(response.status_code, 403)

    def test_get_as_logged_with_right_permissions(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        self.assertFalse(self.user.has_perm('newsletter.delete_comment'))

        self.user.user_permissions.add(Permission.objects.get(name='Can delete comment'))
        response = self.client.get(reverse('newsletter:post-comment-delete', kwargs={'pk': self.post.id}))
        self.assertEqual(response.status_code, 200)

    def test_post_as_logged_with_right_permissions(self):
        """Tests."""
        perms = 'newsletter.delete_comment'
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        self.assertFalse(self.user.has_perm(perms))
        self.user.user_permissions.add(Permission.objects.get(codename=perms.split('.')[1]))

        # Permission caching (https://docs.djangoproject.com/en/2.1/topics/auth/default/#permission-caching)
        # Need to refetch the user to get the new permissions
        self.user = get_user_model().objects.get(id=self.user.id)
        self.assertTrue(self.user.has_perm(perms))

        # Next test
        response = self.client.post(reverse('newsletter:post-comment-delete', kwargs={'pk': self.post.id}))
        self.assertEqual(len(Post.objects.all()), 1)
        self.assertRedirects(response, "/{}/{}/{}/{}/".format(self.post.created.year, self.post.created.month, self.post.created.day, self.post.id), fetch_redirect_response=False)


@tag('comment', 'view', 'delete', 'superuser')
class TestCommentDeleteViewAsSuperuser(TestCase):
    """Tests the modification of a post as superuser.
    
    Unlike simple user or staff user, superuser already has the rights to do whatever he/she wants.
    """

    @classmethod
    def setUpTestData(cls):
        """Set up for all the following tests."""
        cls.dict, cls.user = UserHelper(superuser=True)
        d = {
            'author': cls.user,
            'text': 'Text',
            'title': 'Title'
        }
        cls.post = Post.objects.create(**d)
        cls.comment = Comment.objects.create(post=cls.post, text="Hello World", author=cls.user)

    def test_get_as_logged_with_right_permissions(self):
        """Tests."""
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        self.assertTrue(self.user.has_perm('newsletter.delete_comment'))

        response = self.client.get(reverse('newsletter:post-comment-delete', kwargs={'pk': self.post.id}))
        self.assertEqual(response.status_code, 200)

    def test_post_as_logged_with_right_permissions(self):
        """Tests."""
        perms = 'newsletter.delete_comment'
        self.assertTrue(self.client.login(username=self.dict['username'], password=self.dict['password']))
        self.assertTrue(self.user.has_perm(perms))

        # Next test
        response = self.client.post(reverse('newsletter:post-comment-delete', kwargs={'pk': self.post.id}))
        self.assertEqual(len(Post.objects.all()), 1)
        self.assertRedirects(response, "/{}/{}/{}/{}/".format(self.post.created.year, self.post.created.month, self.post.created.day, self.post.id), fetch_redirect_response=False)
