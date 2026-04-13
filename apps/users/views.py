from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.serializers import SignInSerializer, SignUpSerializer
from apps.users.services import (
    AuthenticationError,
    authenticate_user,
    issue_token,
    revoke_token,
    serialize_authenticated_user,
)


class UsersHealthAPIView(APIView):
    """Users module health endpoint."""

    authentication_classes: list = []
    permission_classes = [AllowAny]

    def get(self, _: Request) -> Response:
        return Response({"status": "users-app-ready"})


class SignUpAPIView(APIView):
    """Create a user account and return API token."""

    authentication_classes: list = []
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = issue_token(user)
        return Response(
            serialize_authenticated_user(user, token),
            status=status.HTTP_201_CREATED,
        )


class SignInAPIView(APIView):
    """Authenticate a user and return API token."""

    authentication_classes: list = []
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        serializer = SignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data
        try:
            user = authenticate_user(email=payload["email"], password=payload["password"])
        except AuthenticationError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        token = issue_token(user)
        return Response(serialize_authenticated_user(user, token), status=status.HTTP_200_OK)


class MeAPIView(APIView):
    """Return current authenticated user info."""

    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        return Response(serialize_authenticated_user(request.user), status=status.HTTP_200_OK)


class SignOutAPIView(APIView):
    """Revoke API token for authenticated user."""

    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        revoke_token(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
