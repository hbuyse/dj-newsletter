# coding=utf-8

"""Views."""

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    ListView
)
from django.views.generic.dates import DateDetailView
from django.views.generic.edit import FormMixin

from .forms import (
    PostCommentForm
)

from .models import (
    Post,
    Comment,
)


class PostListView(ListView):
    """View that returns the list of posts."""

    model = Post
    paginate_by = 10


class PostDetailView(FormMixin, DetailView):
    """Show the details of a post."""

    model = Post
    form_class = PostCommentForm

    def get_success_url(self):
        """."""
        messages.success(self.request, "Comment successfully added")
        return reverse('dj_newsletter:post-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        """Add post_id in request.session."""
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        self.request.session['post_pk'] = self.kwargs['pk']
        return context

    def post(self, request, *args, **kwargs):
        """."""
        if not request.user.is_authenticated:
            raise PermissionDenied
        elif not request.user.has_perm("dj_newsletter.add_comment"):
            raise PermissionDenied
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """Validate the form."""
        form.instance.post = Post.objects.get(id=self.kwargs['pk'])
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


class PostDateDetailView(FormMixin, DateDetailView):
    """Show the details of a post."""

    model = Post
    form_class = PostCommentForm
    date_field = 'created'

    def get_success_url(self):
        """."""
        messages.success(self.request, "Comment successfully added")
        return reverse('dj_newsletter:post-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        """Add post_id in request.session."""
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        self.request.session['post_pk'] = self.kwargs['pk']
        return context

    def post(self, request, *args, **kwargs):
        """."""
        if not request.user.is_authenticated:
            raise PermissionDenied
        elif not request.user.has_perm("dj_newsletter.add_comment"):
            raise PermissionDenied
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """Validate the form."""
        form.instance.post = Post.objects.get(id=self.kwargs['pk'])
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


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
        messages.success(self.request, "Post '{}' added successfully".format(self.object.title))
        return reverse('dj_newsletter:post-detail', kwargs={'pk': self.object.id})


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    """Update a post."""

    model = Post
    fields = ['title', 'text']
    permission_required = 'dj_newsletter.change_post'

    def get_success_url(self):
        """Get the URL after the success."""
        messages.success(self.request, "Post '{}' updated successfully".format(self.object.title))
        return reverse('dj_newsletter:post-detail', kwargs={'pk': self.object.id})


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    """View that allows the deletion of a post."""

    model = Post
    permission_required = 'dj_newsletter.delete_post'

    def get_success_url(self, **kwargs):
        """Get the URL after the success."""
        messages.success(self.request, "Post '{}' deleted successfully".format(self.object.title))
        return reverse('dj_newsletter:posts-list')


class CommentUpdateView(PermissionRequiredMixin, UpdateView):
    """View that allows the modification of a post."""

    model = Comment
    fields = ['text']
    permission_required = 'dj_newsletter.change_comment'

    def get_success_url(self):
        """Get the URL after the success."""
        url = reverse('dj_newsletter:posts-list')

        if 'post_pk' in self.request.session:
            url = reverse('dj_newsletter:post-detail', kwargs={'pk': self.request.session['post_pk']})

        messages.success(self.request, "Comment successfully updated")
        return url


class CommentDeleteView(PermissionRequiredMixin, DeleteView):
    """View that allows the deletion of a post."""

    model = Comment
    fields = ['text']
    permission_required = 'dj_newsletter.delete_comment'

    def get_success_url(self):
        """Get the URL after the success."""
        url = reverse('dj_newsletter:posts-list')

        if 'post_pk' in self.request.session:
            url = reverse('dj_newsletter:post-detail', kwargs={'pk': self.request.session['post_pk']})

        messages.success(self.request, "Comment successfully deleted")
        return url
