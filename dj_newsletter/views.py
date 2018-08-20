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

    def get_context_data(self, **kwargs):
        """Add post_id in request.session."""
        self.request.session['post_pk'] = self.kwargs['pk']
        return super().get_context_data(**kwargs)


class PostCreateView(PermissionRequiredMixin, CreateView):
    """Create a post."""

    model = Post
    fields = ['title', 'text']
    permission_required = 'dj_newsletter.add_post'

    def form_valid(self, form):
        """Validate the form."""
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """Get the URL after the success."""
        return reverse('dj_newsletter:post-detail', kwargs={'pk': self.object.id})


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    """Update a post."""

    model = Post
    fields = ['title', 'text']
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


class CommentCreateView(PermissionRequiredMixin, CreateView):
    """View that allows the creation of a comment."""

    model = Comment
    fields = ['text']
    permission_required = 'dj_newsletter.add_comment'

    def form_valid(self, form):
        """Validate the form."""
        form.instance.post = Post.objects.get(id=self.kwargs['pk'])
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """Get the URL after the success."""
        return reverse('dj_newsletter:post-detail', kwargs={'pk': self.kwargs['pk']})


class CommentUpdateView(PermissionRequiredMixin, UpdateView):
    """View that allows the modification of a post."""

    model = Comment
    fields = ['text']
    permission_required = 'dj_newsletter.change_comment'

    def get_success_url(self):
        """Get the URL after the success."""
        url = str()

        if 'post_pk' in self.request.session:
            url = reverse('dj_newsletter:post-detail', kwargs={'pk': self.request.session['post_pk']})
        else:
            url = reverse('dj_newsletter:posts-list')

        return url


class CommentDeleteView(PermissionRequiredMixin, DeleteView):
    """View that allows the deletion of a post."""

    model = Comment
    fields = ['text']
    permission_required = 'dj_newsletter.delete_comment'

    def get_success_url(self):
        """Get the URL after the success."""
        url = str()

        if 'post_pk' in self.request.session:
            url = reverse('dj_newsletter:post-detail', kwargs={'pk': self.request.session['post_pk']})
        else:
            url = reverse('dj_newsletter:posts-list')

        return url
