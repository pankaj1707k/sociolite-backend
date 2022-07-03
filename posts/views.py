from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView

from posts.models import Post
from posts.serializers import PostSerializer


class PostListCreateView(APIView):
    """
    List existing posts and create new post.
    Allowed methods: GET, POST
    """

    def get(self, request):
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data, HTTP_200_OK)

    def post(self, request):
        serializer = PostSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, HTTP_201_CREATED)


class PostReadUpdateDeleteView(APIView):
    """
    Retrieve, update and delete an individual post.
    Allowed methods: GET, PATCH, DELETE
    """

    def get(self, request, **kwargs):
        post_id = self.kwargs.get("pk")
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            error = {"not found": "post with the provided id does not exist"}
            return Response(error, HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post)
        return Response(serializer.data, HTTP_200_OK)

    def patch(self, request, **kwargs):
        post_id = self.kwargs.get("pk")
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            error = {"not found": "post with the provided id does not exist"}
            return Response(error, HTTP_404_NOT_FOUND)
        if post.author != request.user:
            error = {"access denied": "post is not authored by requesting user"}
            return Response(error, HTTP_401_UNAUTHORIZED)
        serializer = PostSerializer(post, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, HTTP_200_OK)

    def delete(self, request, **kwargs):
        post_id = self.kwargs.get("pk")
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            error = {"not found": "post with the provided id does not exist"}
            return Response(error, HTTP_404_NOT_FOUND)
        if post.author != request.user:
            error = {"access denied": "post is not authored by requesting user"}
            return Response(error, HTTP_401_UNAUTHORIZED)
        post.delete()
        success_message = {"success": "post deleted"}
        return Response(success_message, HTTP_204_NO_CONTENT)
