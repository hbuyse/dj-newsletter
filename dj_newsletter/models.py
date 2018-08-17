# -*- coding: utf-8 -*-
"""Django Newsletter model implementation."""

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


class Post(models.Model):
    """Comment  for Post class."""

    title = models.CharField(_("Post title"), max_length=512)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = MarkdownxField(_('Post text'))
    created = models.DateTimeField('Post creation date', auto_now_add=True)
    modified = models.DateTimeField('Post last modification date', auto_now=True)

    class Meta:
        """Meta class."""

        verbose_name = _("post")
        verbose_name_plural = _("posts")
        ordering = ("-created",)

    def __str__(self):
        """String representation."""
        return self.title

    def text_md(self):
        """Return the text mardownified."""
        return markdownify(self.text)


class Comment(models.Model):
    """Comment  for Post class."""

    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField('Comment creation date', auto_now_add=True)
    modified = models.DateTimeField('Comment last modification date', auto_now=True)
    text = models.TextField(_("Comment text"))

    class Meta:
        """Meta class."""

        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ("post", "-created",)
