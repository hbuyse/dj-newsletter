# coding = utf-8

"""Forms."""

# Django
from django.forms import ModelForm

# Current django project
from newsletter.models import Comment


class PostCommentForm(ModelForm):
    """Comment form for the Mixin."""

    class Meta:
        model = Comment
        fields = ['text']
