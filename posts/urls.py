from django.urls import path

from posts.views import PostListCreateView, PostReadUpdateDeleteView

urlpatterns = [
    path("", PostListCreateView.as_view()),
    path("<int:pk>/", PostReadUpdateDeleteView.as_view()),
]
