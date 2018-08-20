# coding=utf-8

"""urls for the dj-newsletter package."""


from django.urls import path

from . import views


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
    path("<int:pk>/comments",
         view=views.CommentListView.as_view(),
         name='post-comments-list',
         ),
    path("<int:pk>/comments/create",
         view=views.CommentCreateView.as_view(),
         name='post-comment-create',
         ),
    path("comments/<int:pk>",
         view=views.CommentDetailView.as_view(),
         name='post-comment-detail',
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