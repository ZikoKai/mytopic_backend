from django.apps import AppConfig


class CommonConfig(AppConfig):
    """
    Django app config for shared/common components.

    Securite:
    - Centralise le namespace de l'app pour un chargement explicite.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.common"
