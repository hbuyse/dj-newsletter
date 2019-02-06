# -*- coding: utf-8 -*-
"""Django Newsletter model implementation."""

# Third-party
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

# Django
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Post(models.Model):
    """Post model."""

    title = models.CharField(_("Post title"), max_length=512)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text = MarkdownxField(_('Post text'))
    created = models.DateTimeField('Post creation date', auto_now_add=True)
    modified = models.DateTimeField('Post last modification date', auto_now=True)

    class Meta:
        verbose_name = _("post")
        ordering = ("-created",)

    def __str__(self):
        """Representation as a string."""
        return self.title

    def text_md(self):
        """Return the text mardownified."""
        return markdownify(self.text)


class Comment(models.Model):
    """Comment model linked to a Post."""

    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text = models.TextField(_("Comment text"))
    created = models.DateTimeField('Comment creation date', auto_now_add=True)
    modified = models.DateTimeField('Comment last modification date', auto_now=True)

    class Meta:
        verbose_name = _("comment")
        ordering = ("post", "-created",)

    def __str__(self):
        """Representation as a string."""
        return "{} - {} ({})".format(self.post.title, self.author, self.id)
