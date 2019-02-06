#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

# Django
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

# Current django project
from newsletter.models import Comment, Post


class TestPostCreateComment(TestCase):
    """Tests the creation of a comment in the PostDetailView.

    Only testing the post method on post-detail since the get methods are handled in PostDetailView are done in
    TestPostDetailView.
    """

    def setUp(self):
        """Tests."""
        self.user = get_user_model().objects.create_user(username="author", password="author")
        self.post = Post.objects.create(title="My Title", author=self.user, text="## Toto")
        self.dict = {
            'post': self.post,
            'author': self.user,
            'text': "Hello World"
        }

    def test_post_create_comment_view_post_as_anonymous(self):
        """Tests."""
        r = self.client.post(reverse('newsletter:post-detail', kwargs={'pk': self.post.id}), self.dict)
        self.assertEqual(r.status_code, 403)

    def test_post_create_comment_view_post_as_logged_with_wrong_permissions(self):
        """Tests."""
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username="author", password="author"))

        r = self.client.post(reverse('newsletter:post-detail', kwargs={'pk': self.post.id}), self.dict)
        self.assertEqual(r.status_code, 403)

    def test_post_create_comment_view_post_as_logged_with_right_permissions(self):
        """Tests."""
        perms = 'newsletter.add_comment'
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username="author", password="author"))
        self.assertFalse(self.user.has_perm(perms))
        self.user.user_permissions.add(Permission.objects.get(codename=perms.split('.')[1]))

        # Permission caching (https://docs.djangoproject.com/en/2.1/topics/auth/default/#permission-caching)
        # Need to refetch the user to get the new permissions
        self.user = get_user_model().objects.get(id=self.user.id)
        self.assertTrue(self.user.has_perm(perms))

        # Next test
        r = self.client.post(reverse('newsletter:post-detail',
                                     kwargs={'pk': self.post.id}), data=self.dict)
        c = Comment.objects.last()
        self.assertEqual(c.text, 'Hello World')
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, reverse('newsletter:post-detail', kwargs={'pk': self.post.id}))


class TestCommentUpdateView(TestCase):
    """Tests."""

    def setUp(self):
        """Tests."""
        self.user = get_user_model().objects.create_user(username="author", password="author")
        self.post = Post.objects.create(title="My Title", author=self.user, text="## Toto")
        self.dict = {
            'post': self.post,
            'author': self.user,
            'text': "Hello World"
        }
        self.comment = Comment.objects.create(**self.dict)

    def test_comments_update_view_get_as_anonymous(self):
        """Tests."""
        r = self.client.get(reverse('newsletter:post-comment-update', kwargs={'pk': self.comment.id}))
        self.assertEqual(r.status_code, 302)
        self.assertIn('?next=/comments/{}/update'.format(self.comment.id), r.url)

    def test_comments_update_view_post_as_anonymous(self):
        """Tests."""
        r = self.client.post(reverse('newsletter:post-comment-update', kwargs={'pk': self.comment.id}), self.dict)
        self.assertEqual(r.status_code, 302)
        self.assertIn('?next=/comments/{}/update'.format(self.comment.id), r.url)

    def test_comments_update_view_get_as_logged_with_wrong_permissions(self):
        """Tests."""
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username="author", password="author"))

        r = self.client.get(reverse('newsletter:post-comment-update', kwargs={'pk': self.comment.id}))
        self.assertEqual(r.status_code, 403)

    def test_comments_update_view_post_as_logged_with_wrong_permissions(self):
        """Tests."""
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username="author", password="author"))

        r = self.client.post(reverse('newsletter:post-comment-update', kwargs={'pk': self.comment.id}), self.dict)
        self.assertEqual(r.status_code, 403)

    def test_comments_update_view_get_as_logged_with_right_permissions(self):
        """Tests."""
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username="author", password="author"))
        self.assertFalse(self.user.has_perm('newsletter.change_post'))

        self.user.user_permissions.add(Permission.objects.get(name='Can change comment'))
        r = self.client.get(reverse('newsletter:post-comment-update', kwargs={'pk': self.comment.id}))
        self.assertEqual(r.status_code, 200)

    def test_comments_update_view_post_as_logged_with_right_permissions_no_session_data(self):
        """Tests."""
        perms = 'newsletter.change_comment'
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username="author", password="author"))
        self.assertFalse(self.user.has_perm(perms))
        self.user.user_permissions.add(Permission.objects.get(codename=perms.split('.')[1]))

        # Permission caching (https://docs.djangoproject.com/en/2.1/topics/auth/default/#permission-caching)
        # Need to refetch the user to get the new permissions
        self.user = get_user_model().objects.get(id=self.user.id)
        self.assertTrue(self.user.has_perm(perms))

        # Next test
        self.dict['text'] = 'hello world 2'
        r = self.client.post(reverse('newsletter:post-comment-update',
                                     kwargs={'pk': self.comment.id}), data=self.dict)
        c = Comment.objects.get(id=self.comment.id)
        self.assertEqual(c.text, 'hello world 2')
        self.assertEqual(r.status_code, 302)
        self.assertNotIn('post_pk', self.client.session)
        self.assertEqual(r.url, reverse('newsletter:post-list'))

    def test_comments_update_view_post_as_logged_with_right_permissions_with_session_data(self):
        """Tests."""
        perms = 'newsletter.change_comment'
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username="author", password="author"))
        self.assertFalse(self.user.has_perm(perms))
        self.user.user_permissions.add(Permission.objects.get(codename=perms.split('.')[1]))

        # Permission caching (https://docs.djangoproject.com/en/2.1/topics/auth/default/#permission-caching)
        # Need to refetch the user to get the new permissions
        self.user = get_user_model().objects.get(id=self.user.id)
        self.assertTrue(self.user.has_perm(perms))

        # Next test
        self.dict['text'] = 'hello world 2'
        session = self.client.session
        session['post_pk'] = str(self.post.id)
        session.save()
        r = self.client.post(reverse('newsletter:post-comment-update',
                                     kwargs={'pk': self.comment.id}), data=self.dict)
        c = Comment.objects.get(id=self.comment.id)
        self.assertEqual(c.text, 'hello world 2')
        self.assertEqual(r.status_code, 302)
        self.assertIn('post_pk', self.client.session)
        self.assertEqual(r.url, reverse('newsletter:post-detail', kwargs={'pk': self.post.id}))


class TestCommentDeleteView(TestCase):
    """Tests."""

    def setUp(self):
        """Tests."""
        self.user = get_user_model().objects.create_user(username="author", password="author")
        self.post = Post.objects.create(title="My Title", author=self.user, text="## Toto")
        self.dict = {
            'post': self.post,
            'author': self.user,
            'text': "Hello World"
        }
        self.comment = Comment.objects.create(**self.dict)

    def test_comments_delete_view_get_as_anonymous(self):
        """Tests."""
        r = self.client.get(reverse('newsletter:post-comment-delete', kwargs={'pk': self.comment.id}))
        self.assertEqual(r.status_code, 302)
        self.assertIn('?next=/comments/{}/delete'.format(self.post.id), r.url)

    def test_comments_delete_view_post_as_anonymous(self):
        """Tests."""
        r = self.client.post(reverse('newsletter:post-comment-delete', kwargs={'pk': self.comment.id}), self.dict)
        self.assertEqual(r.status_code, 302)
        self.assertIn('?next=/comments/{}/delete'.format(self.post.id), r.url)

    def test_comments_delete_view_get_as_logged_with_wrong_permissions(self):
        """Tests."""
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username="author", password="author"))

        r = self.client.get(reverse('newsletter:post-comment-delete', kwargs={'pk': self.comment.id}))
        self.assertEqual(r.status_code, 403)

    def test_comments_delete_view_post_as_logged_with_wrong_permissions(self):
        """Tests."""
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username="author", password="author"))

        r = self.client.post(reverse('newsletter:post-comment-delete', kwargs={'pk': self.comment.id}), self.dict)
        self.assertEqual(r.status_code, 403)

    def test_comments_delete_view_get_as_logged_with_right_permissions(self):
        """Tests."""
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username="author", password="author"))
        self.assertFalse(self.user.has_perm('newsletter.delete_post'))

        self.user.user_permissions.add(Permission.objects.get(name='Can delete comment'))
        r = self.client.get(reverse('newsletter:post-comment-delete', kwargs={'pk': self.comment.id}))
        self.assertEqual(r.status_code, 200)

    def test_comments_delete_view_post_as_logged_with_right_permissions_no_session_data(self):
        """Tests."""
        perms = 'newsletter.delete_comment'
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username="author", password="author"))
        self.assertFalse(self.user.has_perm(perms))
        self.user.user_permissions.add(Permission.objects.get(codename=perms.split('.')[1]))

        # Permission caching (https://docs.djangoproject.com/en/2.1/topics/auth/default/#permission-caching)
        # Need to refetch the user to get the new permissions
        self.user = get_user_model().objects.get(id=self.user.id)
        self.assertTrue(self.user.has_perm(perms))

        # Next test
        self.assertEqual(Comment.objects.count(), 1)
        r = self.client.post(reverse('newsletter:post-comment-delete', kwargs={'pk': self.comment.id}))
        self.assertEqual(Comment.objects.count(), 0)
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, reverse('newsletter:post-list'))

    def test_comments_delete_view_post_as_logged_with_right_permissions_with_session_data(self):
        """Tests."""
        perms = 'newsletter.delete_comment'
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username="author", password="author"))
        self.assertFalse(self.user.has_perm(perms))
        self.user.user_permissions.add(Permission.objects.get(codename=perms.split('.')[1]))

        # Permission caching (https://docs.djangoproject.com/en/2.1/topics/auth/default/#permission-caching)
        # Need to refetch the user to get the new permissions
        self.user = get_user_model().objects.get(id=self.user.id)
        self.assertTrue(self.user.has_perm(perms))

        # Next test
        self.assertEqual(Comment.objects.count(), 1)
        session = self.client.session
        session['post_pk'] = str(self.post.id)
        session.save()
        r = self.client.post(reverse('newsletter:post-comment-delete',
                                     kwargs={'pk': self.comment.id}), data=self.dict)
        self.assertEqual(Comment.objects.count(), 0)
        self.assertEqual(r.status_code, 302)
        self.assertIn('post_pk', self.client.session)
        self.assertEqual(r.url, reverse('newsletter:post-detail', kwargs={'pk': self.post.id}))
