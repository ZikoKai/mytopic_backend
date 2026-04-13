from django.urls import path

from apps.users.views import (
    MeAPIView,
    SignInAPIView,
    SignOutAPIView,
    SignUpAPIView,
    UsersHealthAPIView,
)


urlpatterns = [
    path("health", UsersHealthAPIView.as_view(), name="users-health"),
    path("auth/sign-up", SignUpAPIView.as_view(), name="users-sign-up"),
    path("auth/sign-in", SignInAPIView.as_view(), name="users-sign-in"),
    path("auth/me", MeAPIView.as_view(), name="users-me"),
    path("auth/sign-out", SignOutAPIView.as_view(), name="users-sign-out"),
]
