from typing import Any

from django.contrib.auth import authenticate, get_user_model
from django.db import transaction
from rest_framework.authtoken.models import Token

from apps.users.models import UserProfile, UserRole


UserModel = get_user_model()


class AuthenticationError(Exception):
    """Raised when authentication credentials are invalid."""


def get_or_create_profile(user: Any) -> UserProfile:
    """Ensure profile existence for a user created before this module."""
    profile, _ = UserProfile.objects.get_or_create(user=user)
    return profile


@transaction.atomic
def create_user_account(email: str, password: str) -> Any:
    """Create an application user with minimal signup information."""
    normalized_email = UserModel.objects.normalize_email(email).strip().lower()
    user = UserModel.objects.create_user(
        username=normalized_email,
        email=normalized_email,
        password=password,
    )
    get_or_create_profile(user)
    return user


def authenticate_user(email: str, password: str) -> Any:
    """Authenticate using email/password mapped to Django username."""
    normalized_email = UserModel.objects.normalize_email(email).strip().lower()
    user = authenticate(username=normalized_email, password=password)
    if user is None:
        raise AuthenticationError("Email ou mot de passe invalide.")
    get_or_create_profile(user)
    return user


def resolve_role(user: Any) -> str:
    """Resolve effective role for API responses."""
    if user.is_staff or user.is_superuser:
        return UserRole.ADMIN
    profile = get_or_create_profile(user)
    return profile.role


def issue_token(user: Any) -> Token:
    """Get or create API token for stateless authentication."""
    token, _ = Token.objects.get_or_create(user=user)
    return token


def revoke_token(user: Any) -> None:
    """Delete current user's API token on sign out."""
    Token.objects.filter(user=user).delete()


def serialize_authenticated_user(user: Any, token: Token | None = None) -> dict[str, Any]:
    """Build a stable auth payload for frontend consumption."""
    display_name = f"{user.first_name} {user.last_name}".strip() or (user.email.split("@")[0] if user.email else "")
    payload: dict[str, Any] = {
        "user": {
            "id": user.id,
            "email": user.email,
            "display_name": display_name,
            "avatar_url": None,
            "role": resolve_role(user),
            "is_admin": user.is_staff or user.is_superuser,
        }
    }
    if token is not None:
        payload["token"] = token.key
    return payload
