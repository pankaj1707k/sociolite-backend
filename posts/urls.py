from django.urls import path

from posts.views import (
    CommentListCreateView,
    CommentReadUpdateDeleteView,
    LikeListCreateView,
    PostListCreateView,
    PostReadUpdateDeleteView,
)

urlpatterns = [
    path("", PostListCreateView.as_view()),
    path("<int:pk>/", PostReadUpdateDeleteView.as_view()),
    path("<int:pid>/comment/", CommentListCreateView.as_view()),
    path("<int:pid>/comment/<int:cid>/", CommentReadUpdateDeleteView.as_view()),
    path("<int:pid>/like/", LikeListCreateView.as_view()),
]
