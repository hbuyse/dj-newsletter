"""..."""

from django.contrib import admin

# Register your models here.
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created')
    date_hierarchy = 'created'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created', 'modified')
    date_hierarchy = 'created'
