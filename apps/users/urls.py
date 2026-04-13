from django.urls import path

from apps.users.views import UsersHealthAPIView


urlpatterns = [
    path("health", UsersHealthAPIView.as_view(), name="users-health"),
]
