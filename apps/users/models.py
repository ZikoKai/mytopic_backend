from django.conf import settings
from django.db import models


class UserRole(models.TextChoices):
    """Supported role values for application authorization."""

    USER = "user", "User"
    ADMIN = "admin", "Admin"


class UserProfile(models.Model):
    """
    Extension model linked to Django auth user.

    Securite:
    - La gestion du mot de passe reste deleguee a django.contrib.auth.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        null=True,
        blank=True,
    )
    role = models.CharField(
        max_length=16,
        choices=UserRole.choices,
        default=UserRole.USER,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users_profile"

    def __str__(self) -> str:
        return f"UserProfile(user_id={self.user_id or 'n/a'}, role={self.role})"
