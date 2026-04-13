"""
URL configuration for Django REST backend.
"""

from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def health(_: object) -> JsonResponse:
    """
    Retourne l'etat de sante de l'API.

    Securite:
    - Endpoint read-only sans donnees sensibles.
    """
    return JsonResponse({"status": "ok", "framework": "django-rest"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("health", health),
    path("api/v1/", include("api.v1.urls")),
]
