from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, logout
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import FollowRelation, Profile
from users.serializers import (
    LoginSerializer,
    PasswordResetSerializer,
    ProfileSerializer,
    UserFollowSerializer,
    UserSerializer,
)
from users.utils import get_token_pair

User = get_user_model()


class UserCreateView(CreateAPIView):
    """Create new User instance"""

    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        headers = self.get_success_headers(serializer.data)
        data = dict(serializer.data)
        data.update(get_token_pair(instance))
        return Response(data, status=HTTP_201_CREATED, headers=headers)


class LoginView(APIView):
    """Authenticate a user and return refresh-access token pair"""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get("username")
        password = serializer.data.get("password")
        user = authenticate(username=username, password=password)
        if user is None:
            msg = {"error": "Invalid credentials"}
            return Response(msg, HTTP_401_UNAUTHORIZED)
        response = {"success": "User authenticated"}
        response.update(get_token_pair(user))
        return Response(response, HTTP_200_OK)


class LogoutView(APIView):
    """Server side logout for user by blacklisting the auth token"""

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            logout(request)
            return Response(status=HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    """
    Get and update user profile.
    Allowed Methods: GET, PATCH
    """

    def get(self, request):
        instance = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(instance)
        return Response(serializer.data, HTTP_200_OK)

    def patch(self, request):
        instance = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(instance, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, HTTP_200_OK)


class PasswordResetView(APIView):
    """
    Request password reset token via email.
    Allowed methods: POST
    """

    def post(self, request):
        from_email = settings.EMAIL_HOST_USER
        to_email = request.user.email
        subject = "Password reset request"
        uid = urlsafe_base64_encode(force_bytes(request.user.id))
        token = PasswordResetTokenGenerator().make_token(request.user)

        message = f"""
            Hello {request.user.name}!
            To reset your password click on the following link:
            http://basehost.domain/password-reset/{uid}/{token}/
        """

        send_mail(subject, message, from_email, [to_email])

        response = {"email": "Instructions to reset password sent to registered email"}
        return Response(response, HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    """
    Check uid and token and change the password.
    Allowed methods: POST
    """

    def post(self, request):
        context = {"request": request}
        serializer = PasswordResetSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        msg = {"success": "Password updated"}
        return Response(msg, HTTP_200_OK)


class FollowUserView(APIView):
    """
    Follow a user.
    Allowed methods: POST
    """

    def post(self, request):
        context = {"request": request}
        serializer = UserFollowSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, HTTP_201_CREATED)


class UnfollowUserView(APIView):
    """
    Unfollow a user.
    Allowed methods: POST
    """

    def post(self, request):
        try:
            obj = FollowRelation.objects.get(
                from_user=request.user, to_user=request.data["to_user"]
            )
        except FollowRelation.DoesNotExist:
            error = {"error": "user not followed"}
            return Response(error, HTTP_400_BAD_REQUEST)
        obj.delete()
        return Response(status=HTTP_204_NO_CONTENT)
