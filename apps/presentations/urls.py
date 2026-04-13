from django.urls import path

from apps.presentations.views import GeneratePresentationAPIView


urlpatterns = [
    path("presentations/generate", GeneratePresentationAPIView.as_view(), name="generate-presentation"),
]
