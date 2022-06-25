from django.contrib.auth import authenticate, get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import LoginSerializer, UserSerializer
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
        refresh = RefreshToken.for_user(instance)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
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
        token_pair = get_token_pair(user)
        response = {
            "success": "User authenticated",
            "refresh": token_pair["refresh"],
            "access": token_pair["access"],
        }
        return Response(response, HTTP_200_OK)
