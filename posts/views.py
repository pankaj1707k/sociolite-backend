from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView
from users.models import FollowRelation

from posts.models import Comment, Like, Post
from posts.serializers import CommentSerializer, LikeSerializer, PostSerializer


class PostListCreateView(APIView):
    """
    List existing posts and create new post.
    Allowed methods: GET, POST
    """

    def get(self, request):
        users = FollowRelation.objects.filter(from_user=request.user)
        users = [obj.to_user for obj in users]
        queryset = Post.objects.filter(author__in=users)
        if not queryset.exists():
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


class CommentListCreateView(APIView):
    """
    List and create comment for given post.
    Allowed methods: GET, POST
    """

    def get(self, request, **kwargs):
        queryset = Comment.objects.filter(post__id=kwargs["pid"])
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data, HTTP_200_OK)

    def post(self, request, **kwargs):
        try:
            post = Post.objects.get(pk=kwargs["pid"])
        except Post.DoesNotExist:
            error = {"not found": "post with the provided id does not exist"}
            return Response(error, HTTP_404_NOT_FOUND)
        serializer_context = {"request": request, "post": post}
        serializer = CommentSerializer(data=request.data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, HTTP_201_CREATED)


class CommentReadUpdateDeleteView(APIView):
    """
    Retrieve, update and delete a comment.
    Allowed methods: GET, PATCH, DELETE
    """

    def get(self, request, **kwargs):
        if not Post.objects.filter(pk=kwargs["pid"]).exists():
            error = {"not found": "post with the provided id does not exist"}
            return Response(error, HTTP_404_NOT_FOUND)
        try:
            comment = Comment.objects.get(pk=kwargs["cid"])
        except Comment.DoesNotExist:
            error = {"not found": "comment with the provided id does not exist"}
            return Response(error, HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, HTTP_200_OK)

    def patch(self, request, **kwargs):
        if not Post.objects.filter(pk=kwargs["pid"]).exists():
            error = {"not found": "post with the provided id does not exist"}
            return Response(error, HTTP_404_NOT_FOUND)
        try:
            comment = Comment.objects.get(pk=kwargs["cid"])
        except Comment.DoesNotExist:
            error = {"not found": "comment with the provided id does not exist"}
            return Response(error, HTTP_404_NOT_FOUND)
        if comment.author != request.user:
            error = {"access denied": "comment is not authored by requesting user"}
            return Response(error, HTTP_401_UNAUTHORIZED)
        serializer = CommentSerializer(comment, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, HTTP_200_OK)

    def delete(self, request, **kwargs):
        if not Post.objects.filter(pk=kwargs["pid"]).exists():
            error = {"not found": "post with the provided id does not exist"}
            return Response(error, HTTP_404_NOT_FOUND)
        try:
            comment = Comment.objects.get(pk=kwargs["cid"])
        except Comment.DoesNotExist:
            error = {"not found": "comment with the provided id does not exist"}
            return Response(error, HTTP_404_NOT_FOUND)
        if comment.author != request.user:
            error = {"access denied": "comment is not authored by requesting user"}
            return Response(error, HTTP_401_UNAUTHORIZED)
        comment.delete()
        success_message = {"success": "comment deleted"}
        return Response(success_message, HTTP_204_NO_CONTENT)


class LikeListCreateView(APIView):
    """
    List and create likes.
    Allowed methods: GET, POST
    """

    def get(self, request, **kwargs):
        queryset = Like.objects.filter(post__id=kwargs["pid"])
        serializer = LikeSerializer(queryset, many=True)
        return Response(serializer.data, HTTP_200_OK)

    def post(self, request, **kwargs):
        try:
            post = Post.objects.get(pk=kwargs["pid"])
        except Post.DoesNotExist:
            error = {"not found": "post with the provided id does not exist"}
            return Response(error, HTTP_404_NOT_FOUND)
        serializer_context = {"request": request, "post": post}
        serializer = LikeSerializer(data=request.data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, HTTP_201_CREATED)


class LikeReadDeleteView(APIView):
    """
    Retrieve and delete an individual like instance.
    Allowed methods: GET, DELETE
    """

    def get(self, request, **kwargs):
        if not Post.objects.filter(pk=kwargs["pid"]).exists():
            error = {"not found": "post with the provided id does not exist"}
            return Response(error, HTTP_404_NOT_FOUND)
        try:
            like = Like.objects.get(pk=kwargs["lid"])
        except Like.DoesNotExist:
            error = {"not found": "like with the provided id does not exist"}
            return Response(error, HTTP_404_NOT_FOUND)
        serializer = LikeSerializer(like)
        return Response(serializer.data, HTTP_200_OK)

    def delete(self, request, **kwargs):
        if not Post.objects.filter(pk=kwargs["pid"]).exists():
            error = {"not found": "post with the provided id does not exist"}
            return Response(error, HTTP_404_NOT_FOUND)
        try:
            like = Like.objects.get(pk=kwargs["lid"])
        except Like.DoesNotExist:
            error = {"not found": "like with the provided id does not exist"}
            return Response(error, HTTP_404_NOT_FOUND)
        if like.author != request.user:
            error = {"access denied": "like is not authored by requesting user"}
            return Response(error, HTTP_401_UNAUTHORIZED)
        like.delete()
        success_message = {"success": "like deleted"}
        return Response(success_message, HTTP_204_NO_CONTENT)


class PostListByUserView(APIView):
    """
    List all posts authored by a user.
    Allowed methods: GET
    """

    def get(self, request, **kwargs):
        queryset = Post.objects.filter(author__id=kwargs["uid"])
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data, HTTP_200_OK)
