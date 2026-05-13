from django.conf import settings
from django.db import models

from apps.ai.crypto import decrypt_secret, encrypt_secret
from apps.ai.types import ProviderType


class AIProviderConfig(models.Model):
    """Per-user LLM provider configuration for private AI mode."""

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ai_provider_configs",
    )
    provider_name = models.CharField(max_length=120)
    provider_type = models.CharField(
        max_length=32,
        choices=[(item.value, item.value) for item in ProviderType],
    )
    base_url = models.URLField(max_length=500, blank=True)
    encrypted_api_key = models.TextField(blank=True)
    model_name = models.CharField(max_length=160)
    temperature = models.FloatField(default=0.85)
    max_tokens = models.PositiveIntegerField(default=5000)
    timeout_ms = models.PositiveIntegerField(default=90000)
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_error = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ai_provider_configs"
        ordering = ["-is_default", "provider_name"]
        indexes = [
            models.Index(fields=["owner", "provider_type"]),
            models.Index(fields=["owner", "is_default"]),
        ]

    def __str__(self) -> str:
        return f"{self.provider_name} ({self.provider_type})"

    @property
    def has_api_key(self) -> bool:
        return bool(self.encrypted_api_key)

    def set_api_key(self, api_key: str) -> None:
        self.encrypted_api_key = encrypt_secret(api_key)

    def get_api_key(self) -> str:
        return decrypt_secret(self.encrypted_api_key)

    def save(self, *args: object, **kwargs: object) -> None:
        super().save(*args, **kwargs)
        if self.is_default:
            AIProviderConfig.objects.filter(owner=self.owner, is_default=True).exclude(
                pk=self.pk,
            ).update(is_default=False)
