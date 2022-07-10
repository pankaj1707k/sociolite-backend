"""base URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView


class EndpointListView(APIView):
    """List all available api endpoints"""

    def get(self, request):
        response = [
            {
                "url": "/api/user/token/",
                "methods": ["POST"],
                "desc": "Get access-refresh token pair for provided user credentials",
            },
            {
                "url": "/api/user/token/refresh/",
                "methods": ["POST"],
                "desc": "Get new access token for provided refresh token if valid",
            },
            {
                "url": "/api/user/register/",
                "methods": ["POST"],
                "desc": "Register new user",
            },
            {
                "url": "/api/user/login/",
                "methods": ["POST"],
                "desc": "Authenticate user with appropriate credentials",
            },
            {
                "url": "/api/user/logout/",
                "methods": ["POST"],
                "desc": "Server side logout for user. Blacklist refresh token",
            },
            {
                "url": "/api/user/profile/",
                "methods": ["GET", "PATCH"],
                "desc": "Get and update profile data",
            },
            {
                "url": "/api/user/password-reset/",
                "methods": ["POST"],
                "desc": "Request password reset token via email",
            },
            {
                "url": "/api/user/password-reset-confirm/",
                "methods": ["POST"],
                "desc": "Check uid and token, and change password",
            },
            {"url": "/api/user/follow/", "methods": ["POST"], "desc": "Follow a user"},
            {
                "url": "/api/user/unfollow/",
                "methods": ["POST"],
                "desc": "Unfollow a user",
            },
            {
                "url": "/api/post/",
                "methods": ["GET", "POST"],
                "desc": "List existing posts and create new post",
            },
            {
                "url": "/api/post/{pid}/",
                "methods": ["GET", "PATCH", "DELETE"],
                "desc": "Retrieve, update and delete an individual post",
            },
            {
                "url": "/api/post/user/{uid}/",
                "methods": ["GET"],
                "desc": "List all posts authored by a user",
            },
            {
                "url": "/api/post/{pid}/comment/",
                "methods": ["GET", "POST"],
                "desc": "List and create comment for given post",
            },
            {
                "url": "/api/post/{pid}/comment/{cid}/",
                "methods": ["GET", "PATCH", "DELETE"],
                "desc": "Retrieve, update and delete a comment",
            },
            {
                "url": "/api/post/{pid}/like/",
                "methods": ["GET", "POST"],
                "desc": "List and create likes",
            },
            {
                "url": "/api/post/{pid}/like/{lid}/",
                "methods": ["GET", "DELETE"],
                "desc": "Retrieve and delete an individual like instance",
            },
        ]

        return Response(response, HTTP_200_OK)


urlpatterns = [
    path("", EndpointListView.as_view()),
    path("admin/", admin.site.urls),
    path("api/user/", include("users.urls")),
    path("api/post/", include("posts.urls")),
]

# Handle media files in development environment
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
