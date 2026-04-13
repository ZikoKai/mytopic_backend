from rest_framework import serializers
from django.contrib.auth import get_user_model

from apps.users.services import create_user_account


UserModel = get_user_model()


class UserReadSerializer(serializers.Serializer):
    """Output serializer for authenticated user payload."""

    id = serializers.IntegerField()
    email = serializers.EmailField()
    role = serializers.ChoiceField(choices=["user", "admin"])
    is_admin = serializers.BooleanField()


class SignUpSerializer(serializers.Serializer):
    """Minimal signup payload: email + password."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8, trim_whitespace=False)

    def validate_email(self, value: str) -> str:
        normalized = value.strip().lower()
        if UserModel.objects.filter(email__iexact=normalized).exists():
            raise serializers.ValidationError("Un compte existe deja pour cet email.")
        return normalized

    def create(self, validated_data: dict) -> object:
        return create_user_account(
            email=validated_data["email"],
            password=validated_data["password"],
        )


class SignInSerializer(serializers.Serializer):
    """Signin payload serializer."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)


class UserSerializer(serializers.Serializer):
    """Backward-compatible serializer alias."""

    id = serializers.IntegerField()
    email = serializers.EmailField()
