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
