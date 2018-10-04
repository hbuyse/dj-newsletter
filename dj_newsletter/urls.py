# coding=utf-8

"""urls for the dj-newsletter package."""


from django.urls import path
from django.views.generic.dates import DateDetailView

from . import views
from .models import Post

app_name = 'dj_newsletter'
urlpatterns = [
    path("",
         view=views.PostListView.as_view(),
         name='posts-list',
         ),
    path("create",
         view=views.PostCreateView.as_view(),
         name='post-create',
         ),
    path("<int:year>/<str:month>/<int:day>/<int:pk>",
         views.PostDateDetailView.as_view(),
         name='post-detail-date',
         ),
    path("<int:pk>",
         view=views.PostDetailView.as_view(),
         name='post-detail',
         ),
    path("<int:pk>/update",
         view=views.PostUpdateView.as_view(),
         name='post-update',
         ),
    path("<int:pk>/delete",
         view=views.PostDeleteView.as_view(),
         name='post-delete',
         ),
    path("comments/<int:pk>/update",
         view=views.CommentUpdateView.as_view(),
         name='post-comment-update',
         ),
    path("comments/<int:pk>/delete",
         view=views.CommentDeleteView.as_view(),
         name='post-comment-delete',
         )
]
