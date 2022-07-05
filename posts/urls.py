from django.urls import path

from posts.views import (
    CommentListCreateView,
    PostListCreateView,
    PostReadUpdateDeleteView,
)

urlpatterns = [
    path("", PostListCreateView.as_view()),
    path("<int:pk>/", PostReadUpdateDeleteView.as_view()),
    path("<int:pid>/comment/", CommentListCreateView.as_view()),
]
