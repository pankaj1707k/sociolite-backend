from django.urls import path

from posts.views import PostListCreateView

urlpatterns = [path("", PostListCreateView.as_view())]
