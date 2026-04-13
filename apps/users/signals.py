from typing import Any

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.users.models import UserProfile


UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def create_user_profile(sender: Any, instance: Any, created: bool, **_: object) -> None:
    """Create profile automatically for newly created users."""
    if created:
        UserProfile.objects.get_or_create(user=instance)
