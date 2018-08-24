# coding = utf-8

"""Forms."""

from django.forms import ModelForm

from .models import (
    Comment
)


class PostCommentForm(ModelForm):
    """Comment form for the Mixin."""

    class Meta:
        model = Comment
        fields = ['text']
