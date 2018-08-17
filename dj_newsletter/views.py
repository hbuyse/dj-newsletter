# coding=utf-8

"""Views."""

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    ListView
)

from .models import (
    Post,
    Comment,
)


class PostListView(ListView):
    """View that returns the list of posts."""

    model = Post
    paginate_by = 10


class PostDetailView(DetailView):
    """Show the details of a post."""

    model = Post


class PostCreateView(PermissionRequiredMixin, CreateView):
    """Create a post."""

    model = Post
    fields = '__all__'
    permission_required = 'dj_newsletter.add_post'

    def get_success_url(self):
        """Get the URL after the success."""
        return reverse('dj_newsletter:post-detail', kwargs={'pk': self.object.id})


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    """Update a post."""

    model = Post
    fields = '__all__'
    permission_required = 'dj_newsletter.change_post'

    def get_success_url(self):
        """Get the URL after the success."""
        return reverse('dj_newsletter:post-detail', kwargs={'pk': self.object.id})


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    """View that allows the deletion of a post."""

    model = Post
    permission_required = 'dj_newsletter.delete_post'

    def get_success_url(self, **kwargs):
        """Get the URL after the success."""
        return reverse('dj_newsletter:posts-list')


class CommentCreateView(CreateView):

    model = Comment


class CommentDeleteView(DeleteView):

    model = Comment


class CommentDetailView(DetailView):

    model = Comment


class CommentUpdateView(UpdateView):

    model = Comment


class CommentListView(ListView):

    model = Comment
