#!/usr/bin/env python
# coding=utf-8

"""Tests for `newsletter` urls module."""

# Django
from django.test import TestCase
from django.urls import reverse


class TestUrlsPost(TestCase):
    """Tests the urls for the newsletter."""

    def test_post_list_url(self):
        """Test the URL of the listing of posts."""
        url = reverse('newsletter:post-list')
        self.assertEqual(url, '/')

    def test_post_create_url(self):
        """Test the URL of that allows the creation of a post."""
        url = reverse('newsletter:post-create')
        self.assertEqual(url, '/create/')

    def test_post_detail_date_url(self):
        """Test the URL that gives the details of a post."""
        url = reverse('newsletter:post-detail-date', kwargs={'year': 2019, 'month': 1, 'day': 23, 'pk': 1})
        self.assertNotEqual(url, "/2018/1/23/1/")
        self.assertNotEqual(url, "/2019/2/23/1/")
        self.assertNotEqual(url, "/2019/1/24/1/")
        self.assertNotEqual(url, "/2019/1/23/2/")
        self.assertEqual(url, '/2019/1/23/1/')

    def test_post_update_url(self):
        """Test the URL of the listing of posts."""
        url = reverse('newsletter:post-update', kwargs={'pk': 1})
        self.assertEqual(url, "/1/update/")

    def test_post_delete_url(self):
        """Test the URL of the listing of posts."""
        url = reverse('newsletter:post-delete', kwargs={'pk': 1})
        self.assertEqual(url, "/1/delete/")


class TestUrlsComment(TestCase):
    """Tests the urls for the newsletter."""

    def test_post_comment_update_url(self):
        """Test the URL of the listing of posts."""
        url = reverse('newsletter:post-comment-update', kwargs={'pk': 1})
        self.assertEqual(url, "/comments/1/update/")

    def test_post_comment_delete_url(self):
        """Test the URL of the listing of posts."""
        url = reverse('newsletter:post-comment-delete', kwargs={'pk': 1})
        self.assertEqual(url, "/comments/1/delete/")
