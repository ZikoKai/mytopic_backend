from django.apps import AppConfig


class AIConfig(AppConfig):
    """
    Django app config for AI generation services.

    Securite:
    - Encadre le chargement de l'app AI dans le runtime Django.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.ai"
