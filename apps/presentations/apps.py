from django.apps import AppConfig


class PresentationsConfig(AppConfig):
    """
    Django app config for presentation endpoints.

    Securite:
    - Declaratif uniquement, sans logique sensible.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.presentations"
