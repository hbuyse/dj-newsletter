#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

from dj_newsletter.models import Post

from django.conf import settings
from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse

import os.path


class TestPostListView(TestCase):
    """Tests."""

    def setUp(self):
        """Tests."""
        self.user = User.objects.create_user(username="username", password="password")

    def test_posts_list_view_empty(self):
        """Tests."""
        r = self.client.get(reverse('dj_newsletter:posts-list'))
        self.assertEqual(r.status_code, 200)
        self.assertIn("No posts...", str(r.content))

    def test_posts_list_view_one_post(self):
        """Tests."""
        Post.objects.create(title="Toto", author=self.user)
        r = self.client.get(reverse('dj_newsletter:post-detail', kwargs={'pk': 1}))
        self.assertEqual(r.status_code, 200)
        self.assertIn("Toto", str(r.content))


# class TestPostDetailView(TestCase):
#     """Tests."""

#     def test_posts_detail_view_not_existing(self):
#         """Tests."""
#         r = self.client.get(reverse('dj_newsletter:post-detail', kwargs={'pk': 1}))
#         self.assertEqual(r.status_code, 404)

#     def test_posts_detail_view(self):
#         """Tests."""
#         Post.objects.create(name="Toto")
#         r = self.client.get(reverse('dj_newsletter:post-detail', kwargs={'pk': 1}))
#         self.assertEqual(r.status_code, 200)
#         self.assertIn("Toto", str(r.content))


# class TestPostCreateView(TestCase):
#     """Tests."""

#     def setUp(self):
#         """Tests."""
#         self.user = User.objects.create_user(username="username", password="password")
#         self.dict = {
#             'name': 'Toto',
#             'summary': 'summary',
#             'description': 'description',
#             'url': 'http://www.google.fr',
#         }
#         pass

#     def teardown_method(self):
#         """Tests."""
#         pass

#     def test_sponsors_create_view_get_as_anonymous(self):
#         """Tests."""
#         r = self.client.get(reverse('dj_newsletter:post-create'))
#         self.assertEqual(r.status_code, 302)
#         self.assertIn('?next=/create', r.url)

#     def test_sponsors_create_view_post_as_anonymous(self):
#         """Tests."""
#         r = self.client.post(reverse('dj_newsletter:post-create'), self.dict)
#         self.assertEqual(r.status_code, 302)
#         self.assertIn('?next=/create', r.url)

#     def test_sponsors_create_view_get_as_logged_with_wrong_permissions(self):
#         """Tests."""
#         self.assertTrue(self.user.is_active)
#         self.assertTrue(self.client.login(username="username", password="password"))

#         r = self.client.get(reverse('dj_newsletter:post-create'))
#         self.assertEqual(r.status_code, 302)
#         self.assertIn('?next=/create', r.url)

#     def test_sponsors_create_view_post_as_logged_with_wrong_permissions(self):
#         """Tests."""
#         self.assertTrue(self.user.is_active)
#         self.assertTrue(self.client.login(username="username", password="password"))

#         r = self.client.post(reverse('dj_newsletter:post-create'), self.dict)
#         self.assertEqual(r.status_code, 302)
#         self.assertIn('?next=/create', r.url)

#     def test_sponsors_create_view_get_as_logged_with_right_permissions(self):
#         """Tests."""
#         self.assertTrue(self.user.is_active)
#         self.assertTrue(self.client.login(username="username", password="password"))
#         self.assertFalse(self.user.has_perm('dj_newsletter.add_sponsor'))

#         self.user.user_permissions.add(Permission.objects.get(name='Can add sponsor'))
#         r = self.client.get(reverse('dj_newsletter:post-create'))
#         self.assertEqual(r.status_code, 200)

#     def test_sponsors_create_view_post_as_logged_with_right_permissions(self):
#         """Tests."""
#         self.assertTrue(self.user.is_active)
#         self.assertTrue(self.client.login(username="username", password="password"))
#         self.assertFalse(self.user.has_perm('dj_newsletter.add_sponsor'))

#         self.user.user_permissions.add(Permission.objects.get(name='Can add sponsor'))
#         r = self.client.post(reverse('dj_newsletter:post-create'), data=self.dict)
#         s = Post.objects.last()
#         self.assertEqual(s.name, "Toto")
#         self.assertEqual(r.status_code, 302)
#         self.assertEqual(r.url, reverse('dj_newsletter:post-detail', kwargs={'pk': s.id}))
#         self.assertTrue(os.path.isfile("{}/sponsors/{}/logo.png".format(settings.MEDIA_ROOT, s.name)))


# class TestPostUpdateView(TestCase):
#     """Tests."""

#     def setUp(self):
#         """Tests."""
#         self.user = User.objects.create_user(username="username", password="password")
#         self.dict = {
#             'name': 'My Toto',
#             'summary': 'My summary',
#             'description': 'My description',
#             'url': 'http://www.google.fr'
#         }
#         self.sponsor = Post.objects.create(**self.dict)
#         pass

#     def teardown_method(self):
#         """Tests."""
#         pass

#     def test_sponsors_update_view_get_as_anonymous(self):
#         """Tests."""
#         r = self.client.get(reverse('dj_newsletter:post-update', kwargs={'pk': self.sponsor.id}))
#         self.assertEqual(r.status_code, 302)
#         self.assertIn('?next=/{}/update'.format(self.sponsor.id), r.url)

#     def test_sponsors_update_view_post_as_anonymous(self):
#         """Tests."""
#         r = self.client.post(reverse('dj_newsletter:post-update', kwargs={'pk': self.sponsor.id}), self.dict)
#         self.assertEqual(r.status_code, 302)
#         self.assertIn('?next=/{}/update'.format(self.sponsor.id), r.url)

#     def test_sponsors_update_view_get_as_logged_with_wrong_permissions(self):
#         """Tests."""
#         self.assertTrue(self.user.is_active)
#         self.assertTrue(self.client.login(username="username", password="password"))

#         r = self.client.get(reverse('dj_newsletter:post-update', kwargs={'pk': self.sponsor.id}))
#         self.assertEqual(r.status_code, 302)
#         self.assertIn('?next=/{}/update'.format(self.sponsor.id), r.url)

#     def test_sponsors_update_view_post_as_logged_with_wrong_permissions(self):
#         """Tests."""
#         self.assertTrue(self.user.is_active)
#         self.assertTrue(self.client.login(username="username", password="password"))

#         r = self.client.post(reverse('dj_newsletter:post-update', kwargs={'pk': self.sponsor.id}), self.dict)
#         self.assertEqual(r.status_code, 302)
#         self.assertIn('?next=/{}/update'.format(self.sponsor.id), r.url)

#     def test_sponsors_update_view_get_as_logged_with_right_permissions(self):
#         """Tests."""
#         self.assertTrue(self.user.is_active)
#         self.assertTrue(self.client.login(username="username", password="password"))
#         self.assertFalse(self.user.has_perm('dj_newsletter.change_sponsor'))

#         self.user.user_permissions.add(Permission.objects.get(name='Can change sponsor'))
#         r = self.client.get(reverse('dj_newsletter:post-update', kwargs={'pk': self.sponsor.id}))
#         self.assertEqual(r.status_code, 200)
#         self.assertEqual(str(r.content).count('<label'), 5)
#         self.assertEqual(str(r.content).count('</label>'), 5)
#         self.assertIn('Post name', str(r.content))
#         self.assertIn('Toto', str(r.content))
#         self.assertIn('Post summary', str(r.content))
#         self.assertIn('My summary', str(r.content))
#         self.assertIn('Post description', str(r.content))
#         self.assertIn('My description', str(r.content))
#         self.assertIn('Post logo', str(r.content))
#         self.assertIn('logo.png', str(r.content))
#         self.assertIn('Post url', str(r.content))
#         self.assertIn('http://www.google.fr', str(r.content))

#     def test_sponsors_update_view_post_as_logged_with_right_permissions(self):
#         """Tests."""
#         self.assertTrue(self.user.is_active)
#         self.assertTrue(self.client.login(username="username", password="password"))
#         self.assertFalse(self.user.has_perm('dj_newsletter.change_sponsor'))

#         self.user.user_permissions.add(Permission.objects.get(name='Can change sponsor'))
#         self.dict['name'] = 'Toto new'
#         self.dict['logo'] = SimpleUploadedFile(name='index.png',
#                                                content=open("dj_newsletter/tests/index.png", 'rb').read(),
#                                                content_type='image/png')

#         r = self.client.post(reverse('dj_newsletter:post-update', kwargs={'pk': self.sponsor.id}), data=self.dict)
#         s = Post.objects.get(id=self.sponsor.id)
#         self.assertEqual(s.name, "Toto new")
#         self.assertEqual(r.status_code, 302)
#         self.assertEqual(r.url, reverse('dj_newsletter:post-detail', kwargs={'pk': s.id}))
#         self.assertTrue(os.path.isfile("{}/sponsors/{}/logo.png".format(settings.MEDIA_ROOT, s.name)))


# class TestPostDeleteView(TestCase):
#     """Tests."""

#     def setUp(self):
#         """Tests."""
#         self.user = User.objects.create_user(username="username", password="password")
#         self.dict = {
#             'name': 'My Toto',
#             'summary': 'My summary',
#             'description': 'My description',
#             'url': 'http://www.google.fr',
#         }
#         self.sponsor = Post.objects.create(**self.dict)
#         pass

#     def teardown_method(self):
#         """Tests."""
#         pass

#     def test_sponsors_delete_view_get_as_anonymous(self):
#         """Tests."""
#         r = self.client.get(reverse('dj_newsletter:post-delete', kwargs={'pk': self.sponsor.id}))
#         self.assertEqual(r.status_code, 302)
#         self.assertIn('?next=/{}/delete'.format(self.sponsor.id), r.url)

#     def test_sponsors_delete_view_post_as_anonymous(self):
#         """Tests."""
#         r = self.client.post(reverse('dj_newsletter:post-delete', kwargs={'pk': self.sponsor.id}), self.dict)
#         self.assertEqual(r.status_code, 302)
#         self.assertIn('?next=/{}/delete'.format(self.sponsor.id), r.url)

#     def test_sponsors_delete_view_get_as_logged_with_wrong_permissions(self):
#         """Tests."""
#         self.assertTrue(self.user.is_active)
#         self.assertTrue(self.client.login(username="username", password="password"))

#         r = self.client.get(reverse('dj_newsletter:post-delete', kwargs={'pk': self.sponsor.id}))
#         self.assertEqual(r.status_code, 302)
#         self.assertIn('?next=/{}/delete'.format(self.sponsor.id), r.url)

#     def test_sponsors_delete_view_post_as_logged_with_wrong_permissions(self):
#         """Tests."""
#         self.assertTrue(self.user.is_active)
#         self.assertTrue(self.client.login(username="username", password="password"))

#         r = self.client.post(reverse('dj_newsletter:post-delete', kwargs={'pk': self.sponsor.id}), self.dict)
#         self.assertEqual(r.status_code, 302)
#         self.assertIn('?next=/{}/delete'.format(self.sponsor.id), r.url)

#     def test_sponsors_delete_view_get_as_logged_with_right_permissions(self):
#         """Tests."""
#         self.assertTrue(self.user.is_active)
#         self.assertTrue(self.client.login(username="username", password="password"))
#         self.assertFalse(self.user.has_perm('dj_newsletter.delete_sponsor'))

#         self.user.user_permissions.add(Permission.objects.get(name='Can delete sponsor'))
#         r = self.client.get(reverse('dj_newsletter:post-delete', kwargs={'pk': self.sponsor.id}))
#         self.assertEqual(r.status_code, 200)
#         self.assertIn("<h1 class=\"float-left\">{}</h1>".format(self.sponsor.name), str(r.content))
#         self.assertIn("<p>Do you really want to delete that sponsor?</p>", str(r.content))

#     def test_sponsors_delete_view_post_as_logged_with_right_permissions(self):
#         """Tests."""
#         self.assertTrue(self.user.is_active)
#         self.assertTrue(self.client.login(username="username", password="password"))
#         self.assertFalse(self.user.has_perm('dj_newsletter.delete_sponsor'))

#         self.user.user_permissions.add(Permission.objects.get(name='Can delete sponsor'))
#         self.assertEqual(Post.objects.count(), 1)
#         r = self.client.post(reverse('dj_newsletter:post-delete', kwargs={'pk': self.sponsor.id}))
#         self.assertEqual(Post.objects.count(), 0)
#         self.assertEqual(r.status_code, 302)
#         self.assertEqual(r.url, reverse('dj_newsletter:sponsors-list'))
