from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import (
    FollowUserView,
    LoginView,
    LogoutView,
    PasswordResetConfirmView,
    PasswordResetView,
    ProfileView,
    UnfollowUserView,
    UserCreateView,
)

urlpatterns = [
    path("token/", TokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("register/", UserCreateView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("profile/", ProfileView.as_view()),
    path("password-reset/", PasswordResetView.as_view()),
    path("password-reset-confirm/", PasswordResetConfirmView.as_view()),
    path("follow/", FollowUserView.as_view()),
    path("unfollow/", UnfollowUserView.as_view()),
]
