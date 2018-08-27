#! /usr/bin/env python
# coding=utf-8

"""Tests the views."""

from dj_newsletter.models import Post, Comment

from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class TestPostListView(TestCase):
    """Tests ListView for Post."""

    def setUp(self):
        """Tests."""
        self.user = get_user_model().objects.create_user(username="author", password="author")

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


class TestPostDetailView(TestCase):
    """Tests DetailView for Post."""

    def setUp(self):
        """Tests."""
        self.user = get_user_model().objects.create_user(username="author", password="author")

    def test_posts_detail_view_not_existing(self):
        """Tests."""
        r = self.client.get(reverse('dj_newsletter:post-detail', kwargs={'pk': 1}))
        self.assertEqual(r.status_code, 404)

    def test_posts_detail_view(self):
        """Tests."""
        p = Post.objects.create(title="My Title", author=self.user, text="## Toto")
        r = self.client.get(reverse('dj_newsletter:post-detail', kwargs={'pk': p.id}))
        self.assertEqual(r.status_code, 200)
        self.assertIn("Toto", str(r.content))
        session = self.client.session
        self.assertIn('post_pk', session)
        self.assertEqual(session['post_pk'], p.id)


class TestPostCreateView(TestCase):
    """Tests."""

    def setUp(self):
        """Tests."""
        self.user = get_user_model().objects.create_user(username="author", password="author")
        self.dict = {
            'title': "My Title",
            'text': "## Toto"
        }

    def test_posts_create_view_get_as_anonymous(self):
        """Tests."""
        r = self.client.get(reverse('dj_newsletter:post-create'))
        self.assertEqual(r.status_code, 302)
        self.assertIn('?next=/create', r.url)

    def test_posts_create_view_post_as_anonymous(self):
        """Tests."""
        r = self.client.post(reverse('dj_newsletter:post-create'), self.dict)
        self.assertEqual(r.status_code, 302)
        self.assertIn('?next=/create', r.url)

    def test_posts_create_view_get_as_logged_with_wrong_permissions(self):
        """Tests."""
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username="author", password="author"))

        r = self.client.get(reverse('dj_newsletter:post-create'))
        self.assertEqual(r.status_code, 302)
        self.assertIn('?next=/create', r.url)

    def test_posts_create_view_post_as_logged_with_wrong_permissions(self):
        """Tests."""
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username="author", password="author"))

        r = self.client.post(reverse('dj_newsletter:post-create'), self.dict)
        self.assertEqual(r.status_code, 302)
        self.assertIn('?next=/create', r.url)

    def test_posts_create_view_get_as_logged_with_right_permissions(self):
        """Tests."""
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username="author", password="author"))
        self.assertFalse(self.user.has_perm('dj_newsletter.add_post'))

        self.user.user_permissions.add(Permission.objects.get(name='Can add post'))
        r = self.client.get(reverse('dj_newsletter:post-create'))
        self.assertEqual(r.status_code, 200)

    def test_posts_create_view_post_as_logged_with_right_permissions(self):
        """Tests."""
        perms = 'dj_newsletter.add_post'
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username="author", password="author"))
        self.assertFalse(self.user.has_perm(perms))
        self.user.user_permissions.add(Permission.objects.get(codename=perms.split('.')[1]))

        # Permission caching (https://docs.djangoproject.com/en/2.1/topics/auth/default/#permission-caching)
        # Need to refetch the user to get the new permissions
        self.user = get_user_model().objects.get(id=self.user.id)
        self.assertTrue(self.user.has_perm(perms))

        # Next test
        r = self.client.post(reverse('dj_newsletter:post-create'), data=self.dict)
        p = Post.objects.last()
        self.assertEqual(p.title, "My Title")
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, reverse('dj_newsletter:post-detail', kwargs={'pk': p.id}))


class TestPostUpdateView(TestCase):
    """Tests."""

    def setUp(self):
        """Tests."""
        self.user = get_user_model().objects.create_user(username="author", password="author")
        self.dict = {
            'title': "My Title",
            'author': self.user,
            'text': "## Toto"
        }
        self.post = Post.objects.create(**self.dict)

    def test_posts_update_view_get_as_anonymous(self):
        """Tests."""
        r = self.client.get(reverse('dj_newsletter:post-update', kwargs={'pk': self.post.id}))
        self.assertEqual(r.status_code, 302)
        self.assertIn('?next=/{}/update'.format(self.post.id), r.url)

    def test_posts_update_view_post_as_anonymous(self):
        """Tests."""
        r = self.client.post(reverse('dj_newsletter:post-update', kwargs={'pk': self.post.id}), self.dict)
        self.assertEqual(r.status_code, 302)
        self.assertIn('?next=/{}/update'.format(self.post.id), r.url)

    def test_posts_update_view_get_as_logged_with_wrong_permissions(self):
        """Tests."""
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username="author", password="author"))

        r = self.client.get(reverse('dj_newsletter:post-update', kwargs={'pk': self.post.id}))
        self.assertEqual(r.status_code, 302)
        self.assertIn('?next=/{}/update'.format(self.post.id), r.url)

    def test_posts_update_view_post_as_logged_with_wrong_permissions(self):
        """Tests."""
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username="author", password="author"))

        r = self.client.post(reverse('dj_newsletter:post-update', kwargs={'pk': self.post.id}), self.dict)
        self.assertEqual(r.status_code, 302)
        self.assertIn('?next=/{}/update'.format(self.post.id), r.url)

    def test_posts_update_view_get_as_logged_with_right_permissions(self):
        """Tests."""
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username="author", password="author"))
        self.assertFalse(self.user.has_perm('dj_newsletter.change_post'))

        self.user.user_permissions.add(Permission.objects.get(name='Can change post'))
        r = self.client.get(reverse('dj_newsletter:post-update', kwargs={'pk': self.post.id}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(str(r.content).count('<label'), 2)
        self.assertEqual(str(r.content).count('</label>'), 2)
        self.assertIn('Post title', str(r.content))
        self.assertIn('My Title', str(r.content))
        self.assertIn('Post text', str(r.content))
        self.assertIn('# Toto', str(r.content))

    def test_posts_update_view_post_as_logged_with_right_permissions(self):
        """Tests."""
        perms = 'dj_newsletter.change_post'
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username="author", password="author"))
        self.assertFalse(self.user.has_perm(perms))
        self.user.user_permissions.add(Permission.objects.get(codename=perms.split('.')[1]))

        # Permission caching (https://docs.djangoproject.com/en/2.1/topics/auth/default/#permission-caching)
        # Need to refetch the user to get the new permissions
        self.user = get_user_model().objects.get(id=self.user.id)
        self.assertTrue(self.user.has_perm(perms))

        # Next test
        self.dict['title'] = 'Toto new'
        r = self.client.post(reverse('dj_newsletter:post-update', kwargs={'pk': self.post.id}), data=self.dict)
        p = Post.objects.get(id=self.post.id)
        self.assertEqual(p.title, "Toto new")
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, reverse('dj_newsletter:post-detail', kwargs={'pk': p.id}))


class TestPostDeleteView(TestCase):
    """Tests."""

    def setUp(self):
        """Tests."""
        self.user = get_user_model().objects.create_user(username="author", password="author")
        self.dict = {
            'title': "My Title",
            'author': self.user,
            'text': "## Toto"
        }
        self.post = Post.objects.create(**self.dict)

    def test_posts_delete_view_get_as_anonymous(self):
        """Tests."""
        r = self.client.get(reverse('dj_newsletter:post-delete', kwargs={'pk': self.post.id}))
        self.assertEqual(r.status_code, 302)
        self.assertIn('?next=/{}/delete'.format(self.post.id), r.url)

    def test_posts_delete_view_post_as_anonymous(self):
        """Tests."""
        r = self.client.post(reverse('dj_newsletter:post-delete', kwargs={'pk': self.post.id}), self.dict)
        self.assertEqual(r.status_code, 302)
        self.assertIn('?next=/{}/delete'.format(self.post.id), r.url)

    def test_posts_delete_view_get_as_logged_with_wrong_permissions(self):
        """Tests."""
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username="author", password="author"))

        r = self.client.get(reverse('dj_newsletter:post-delete', kwargs={'pk': self.post.id}))
        self.assertEqual(r.status_code, 302)
        self.assertIn('?next=/{}/delete'.format(self.post.id), r.url)

    def test_posts_delete_view_post_as_logged_with_wrong_permissions(self):
        """Tests."""
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username="author", password="author"))

        r = self.client.post(reverse('dj_newsletter:post-delete', kwargs={'pk': self.post.id}), self.dict)
        self.assertEqual(r.status_code, 302)
        self.assertIn('?next=/{}/delete'.format(self.post.id), r.url)

    def test_posts_delete_view_get_as_logged_with_right_permissions(self):
        """Tests."""
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username="author", password="author"))
        self.assertFalse(self.user.has_perm('dj_newsletter.delete_post'))

        self.user.user_permissions.add(Permission.objects.get(name='Can delete post'))
        r = self.client.get(reverse('dj_newsletter:post-delete', kwargs={'pk': self.post.id}))
        self.assertEqual(r.status_code, 200)
        self.assertIn("<h1 class=\"float-left\">{}</h1>".format(self.post.title), str(r.content))
        self.assertIn("<p>Do you really want to delete that post and its comments?</p>", str(r.content))

    def test_posts_delete_view_post_as_logged_with_right_permissions(self):
        """Tests."""
        perms = 'dj_newsletter.delete_post'
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username="author", password="author"))
        self.assertFalse(self.user.has_perm(perms))
        self.user.user_permissions.add(Permission.objects.get(codename=perms.split('.')[1]))

        # Permission caching (https://docs.djangoproject.com/en/2.1/topics/auth/default/#permission-caching)
        # Need to refetch the user to get the new permissions
        self.user = get_user_model().objects.get(id=self.user.id)
        self.assertTrue(self.user.has_perm(perms))

        # Next test
        self.assertEqual(Post.objects.count(), 1)
        r = self.client.post(reverse('dj_newsletter:post-delete', kwargs={'pk': self.post.id}))
        self.assertEqual(Post.objects.count(), 0)
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, reverse('dj_newsletter:posts-list'))


class TestPostCreateComment(TestCase):
    """Tests the creation of a comment in the PostDetailView.

    Only testing the posts method on post-detail since the get methods are handled in PostDetailView are done in
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
        r = self.client.post(reverse('dj_newsletter:post-detail', kwargs={'pk': self.post.id}), self.dict)
        self.assertEqual(r.status_code, 403)

    def test_post_create_comment_view_post_as_logged_with_wrong_permissions(self):
        """Tests."""
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username="author", password="author"))

        r = self.client.post(reverse('dj_newsletter:post-detail', kwargs={'pk': self.post.id}), self.dict)
        self.assertEqual(r.status_code, 403)

    def test_post_create_comment_view_post_as_logged_with_right_permissions(self):
        """Tests."""
        perms = 'dj_newsletter.add_comment'
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username="author", password="author"))
        self.assertFalse(self.user.has_perm(perms))
        self.user.user_permissions.add(Permission.objects.get(codename=perms.split('.')[1]))

        # Permission caching (https://docs.djangoproject.com/en/2.1/topics/auth/default/#permission-caching)
        # Need to refetch the user to get the new permissions
        self.user = get_user_model().objects.get(id=self.user.id)
        self.assertTrue(self.user.has_perm(perms))

        # Next test
        r = self.client.post(reverse('dj_newsletter:post-detail',
                                     kwargs={'pk': self.post.id}), data=self.dict)
        c = Comment.objects.last()
        self.assertEqual(c.text, 'Hello World')
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, reverse('dj_newsletter:post-detail', kwargs={'pk': self.post.id}))


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
        r = self.client.get(reverse('dj_newsletter:post-comment-update', kwargs={'pk': self.comment.id}))
        self.assertEqual(r.status_code, 302)
        self.assertIn('?next=/comments/{}/update'.format(self.comment.id), r.url)

    def test_comments_update_view_post_as_anonymous(self):
        """Tests."""
        r = self.client.post(reverse('dj_newsletter:post-comment-update', kwargs={'pk': self.comment.id}), self.dict)
        self.assertEqual(r.status_code, 302)
        self.assertIn('?next=/comments/{}/update'.format(self.comment.id), r.url)

    def test_comments_update_view_get_as_logged_with_wrong_permissions(self):
        """Tests."""
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username="author", password="author"))

        r = self.client.get(reverse('dj_newsletter:post-comment-update', kwargs={'pk': self.comment.id}))
        self.assertEqual(r.status_code, 302)
        self.assertIn('?next=/comments/{}/update'.format(self.comment.id), r.url)

    def test_comments_update_view_post_as_logged_with_wrong_permissions(self):
        """Tests."""
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username="author", password="author"))

        r = self.client.post(reverse('dj_newsletter:post-comment-update', kwargs={'pk': self.comment.id}), self.dict)
        self.assertEqual(r.status_code, 302)
        self.assertIn('?next=/comments/{}/update'.format(self.comment.id), r.url)

    def test_comments_update_view_get_as_logged_with_right_permissions(self):
        """Tests."""
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username="author", password="author"))
        self.assertFalse(self.user.has_perm('dj_newsletter.change_post'))

        self.user.user_permissions.add(Permission.objects.get(name='Can change comment'))
        r = self.client.get(reverse('dj_newsletter:post-comment-update', kwargs={'pk': self.comment.id}))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(str(r.content).count('<label'), 1)
        self.assertEqual(str(r.content).count('</label>'), 1)
        self.assertIn('Comment text', str(r.content))
        self.assertIn('Hello World', str(r.content))

    def test_comments_update_view_post_as_logged_with_right_permissions_no_session_data(self):
        """Tests."""
        perms = 'dj_newsletter.change_comment'
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
        r = self.client.post(reverse('dj_newsletter:post-comment-update',
                                     kwargs={'pk': self.comment.id}), data=self.dict)
        c = Comment.objects.get(id=self.comment.id)
        self.assertEqual(c.text, 'hello world 2')
        self.assertEqual(r.status_code, 302)
        self.assertNotIn('post_pk', self.client.session)
        self.assertEqual(r.url, reverse('dj_newsletter:posts-list'))

    def test_comments_update_view_post_as_logged_with_right_permissions_with_session_data(self):
        """Tests."""
        perms = 'dj_newsletter.change_comment'
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
        r = self.client.post(reverse('dj_newsletter:post-comment-update',
                                     kwargs={'pk': self.comment.id}), data=self.dict)
        c = Comment.objects.get(id=self.comment.id)
        self.assertEqual(c.text, 'hello world 2')
        self.assertEqual(r.status_code, 302)
        self.assertIn('post_pk', self.client.session)
        self.assertEqual(r.url, reverse('dj_newsletter:post-detail', kwargs={'pk': self.post.id}))


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
        r = self.client.get(reverse('dj_newsletter:post-comment-delete', kwargs={'pk': self.comment.id}))
        self.assertEqual(r.status_code, 302)
        self.assertIn('?next=/comments/{}/delete'.format(self.post.id), r.url)

    def test_comments_delete_view_post_as_anonymous(self):
        """Tests."""
        r = self.client.post(reverse('dj_newsletter:post-comment-delete', kwargs={'pk': self.comment.id}), self.dict)
        self.assertEqual(r.status_code, 302)
        self.assertIn('?next=/comments/{}/delete'.format(self.post.id), r.url)

    def test_comments_delete_view_get_as_logged_with_wrong_permissions(self):
        """Tests."""
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username="author", password="author"))

        r = self.client.get(reverse('dj_newsletter:post-comment-delete', kwargs={'pk': self.comment.id}))
        self.assertEqual(r.status_code, 302)
        self.assertIn('?next=/comments/{}/delete'.format(self.post.id), r.url)

    def test_comments_delete_view_post_as_logged_with_wrong_permissions(self):
        """Tests."""
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username="author", password="author"))

        r = self.client.post(reverse('dj_newsletter:post-comment-delete', kwargs={'pk': self.comment.id}), self.dict)
        self.assertEqual(r.status_code, 302)
        self.assertIn('?next=/comments/{}/delete'.format(self.post.id), r.url)

    def test_comments_delete_view_get_as_logged_with_right_permissions(self):
        """Tests."""
        self.assertTrue(self.user.is_active)
        self.assertTrue(self.client.login(username="author", password="author"))
        self.assertFalse(self.user.has_perm('dj_newsletter.delete_post'))

        self.user.user_permissions.add(Permission.objects.get(name='Can delete comment'))
        r = self.client.get(reverse('dj_newsletter:post-comment-delete', kwargs={'pk': self.comment.id}))
        self.assertEqual(r.status_code, 200)
        self.assertIn("<h1 class=\"float-left\">{}</h1>".format(self.comment), str(r.content))
        self.assertIn("<p>Do you really want to delete that comment?</p>", str(r.content))

    def test_comments_delete_view_post_as_logged_with_right_permissions_no_session_data(self):
        """Tests."""
        perms = 'dj_newsletter.delete_comment'
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
        r = self.client.post(reverse('dj_newsletter:post-comment-delete', kwargs={'pk': self.comment.id}))
        self.assertEqual(Comment.objects.count(), 0)
        self.assertEqual(r.status_code, 302)
        self.assertEqual(r.url, reverse('dj_newsletter:posts-list'))

    def test_comments_delete_view_post_as_logged_with_right_permissions_with_session_data(self):
        """Tests."""
        perms = 'dj_newsletter.delete_comment'
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
        r = self.client.post(reverse('dj_newsletter:post-comment-delete',
                                     kwargs={'pk': self.comment.id}), data=self.dict)
        self.assertEqual(Comment.objects.count(), 0)
        self.assertEqual(r.status_code, 302)
        self.assertIn('post_pk', self.client.session)
        self.assertEqual(r.url, reverse('dj_newsletter:post-detail', kwargs={'pk': self.post.id}))
