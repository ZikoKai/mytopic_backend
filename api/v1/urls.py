"""
API v1 URL mappings.
"""

from django.urls import include, path


urlpatterns = [
    path("ai/", include("apps.ai.urls")),
    path("", include("apps.presentations.urls")),
    path("users/", include("apps.users.urls")),
    path("slides/", include("apps.slides.urls")),
    path("designs/", include("apps.designs.urls")),
]
