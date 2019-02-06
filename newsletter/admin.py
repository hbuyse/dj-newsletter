# -*- coding: utf-8
"""Administrative representation of the `newsletter` models."""

# Django
from django.contrib import admin

# Current django project
from newsletter.models import Comment, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Post admin object."""

    list_display = (
        'title',
        'author',
        'created'
    )
    date_hierarchy = 'created'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Comment admin object."""

    list_display = (
        'post',
        'author',
        'created',
        'modified'
    )
    date_hierarchy = 'created'
