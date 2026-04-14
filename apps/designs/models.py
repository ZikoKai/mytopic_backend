import uuid

from django.conf import settings
from django.db import models


class DesignDocument(models.Model):
    """Document de design editable associe a un utilisateur."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="design_documents",
    )
    title = models.CharField(max_length=255)
    content = models.JSONField(default=dict)
    current_version = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "design_documents"
        ordering = ["-updated_at"]

    def __str__(self) -> str:
        return f"DesignDocument(id={self.id}, owner={self.owner_id}, title={self.title})"


class DesignDocumentVersion(models.Model):
    """Snapshot versionne d'un document de design."""

    id = models.BigAutoField(primary_key=True)
    document = models.ForeignKey(
        DesignDocument,
        on_delete=models.CASCADE,
        related_name="versions",
    )
    version_number = models.PositiveIntegerField()
    content = models.JSONField(default=dict)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="design_document_versions",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "design_document_versions"
        ordering = ["-version_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["document", "version_number"],
                name="uniq_design_document_version_number",
            )
        ]

    def __str__(self) -> str:
        return (
            f"DesignDocumentVersion(document={self.document_id}, "
            f"version={self.version_number})"
        )
