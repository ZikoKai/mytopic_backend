from django.urls import path

from apps.slides.views import SlidesHealthAPIView


urlpatterns = [
    path("health", SlidesHealthAPIView.as_view(), name="slides-health"),
]
