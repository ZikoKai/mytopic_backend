from django.db import models
from django.conf import settings
import uuid


class PresentationRequestLog(models.Model):
    """
    Trace minimale des demandes de generation (scaffold migration).

    Securite:
    - Stocke uniquement des metadonnees non sensibles.
    """

    topic = models.CharField(max_length=500)
    language = models.CharField(max_length=64, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "presentation_request_logs"


class PresentationDocument(models.Model):
    """Presentation persistante d'un utilisateur."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="presentation_documents",
    )
    title = models.CharField(max_length=255)
    content = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "presentation_documents"
        ordering = ["-updated_at"]

    def __str__(self) -> str:
        return f"PresentationDocument(id={self.id}, owner={self.owner_id}, title={self.title})"


class FavoriteImageAsset(models.Model):
    """Image favorite reusable across presentations for one user."""

    id = models.UUIDField(primary_key=
    True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorite_image_assets",
    )
    title = models.CharField(max_length=255, blank=True, default="")
    prompt = models.CharField(max_length=1200, blank=True, default="")
    image_data_url = models.TextField()
    mime_type = models.CharField(max_length=64, blank=True, default="image/png")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "favorite_image_assets"
        ordering = ["-updated_at"]

    def __str__(self) -> str:
        return f"FavoriteImageAsset(id={self.id}, owner={self.owner_id})"
