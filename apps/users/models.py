from django.db import models


class UserProfile(models.Model):
    """
    User profile scaffold for future migration steps.

    Securite:
    - Stocke des metadonnees minimales sans dupliquer l'auth core.
    """

    email = models.EmailField(unique=True)
    display_name = models.CharField(max_length=120, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
