#!/usr/bin/env python
# coding=utf-8

"""Tests for `dj-newsletter` urls module."""

from django.test import TestCase
from django.urls import reverse


class TestUrlsPost(TestCase):
    """Tests the urls for the dj-newsletter."""

    def test_post_list_url(self):
        """Test the URL of the listing of posts."""
        url = reverse('dj_newsletter:posts-list')
        self.assertEqual(url, '/')

    def test_post_create_url(self):
        """Test the URL of that allows the creation of a post."""
        url = reverse('dj_newsletter:post-create')
        self.assertEqual(url, '/create')

    def test_post_detail_url(self):
        """Test the URL that gives the details of a post."""
        url = reverse('dj_newsletter:post-detail', kwargs={'pk': 1})
        self.assertEqual(url, '/1')

    def test_post_update_url(self):
        """Test the URL of the listing of posts."""
        url = reverse('dj_newsletter:post-update', kwargs={'pk': 1})
        self.assertEqual(url, "/1/update")

    def test_post_delete_url(self):
        """Test the URL of the listing of posts."""
        url = reverse('dj_newsletter:post-delete', kwargs={'pk': 1})
        self.assertEqual(url, "/1/delete")


class TestUrlsComment(TestCase):
    """Tests the urls for the dj-newsletter."""

    def test_post_list_comments_url(self):
        """Test the URL of the listing of posts."""
        url = reverse('dj_newsletter:post-comments-list', kwargs={'pk': 1})
        self.assertEqual(url, "/1/comments")

    def test_post_comment_create_url(self):
        """Test the URL that adds a comment to a specific post."""
        url = reverse('dj_newsletter:post-comment-create', kwargs={'pk': 1})
        self.assertEqual(url, '/1/comments/create')

    def test_post_comment_detail_url(self):
        """Test the URL of the listing of posts."""
        url = reverse('dj_newsletter:post-comment-detail', kwargs={'pk': 1})
        self.assertEqual(url, '/comments/1')

    def test_post_comment_update_url(self):
        """Test the URL of the listing of posts."""
        url = reverse('dj_newsletter:post-comment-update', kwargs={'pk': 1})
        self.assertEqual(url, "/comments/1/update")

    def test_post_comment_delete_url(self):
        """Test the URL of the listing of posts."""
        url = reverse('dj_newsletter:post-comment-delete', kwargs={'pk': 1})
        self.assertEqual(url, "/comments/1/delete")
