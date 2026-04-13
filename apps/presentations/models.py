from django.db import models


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
