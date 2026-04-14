from django.urls import path

from apps.presentations.views import (
    GeneratePresentationAPIView,
    PresentationDocumentDetailAPIView,
    PresentationDocumentListCreateAPIView,
)


urlpatterns = [
    path("presentations/generate", GeneratePresentationAPIView.as_view(), name="generate-presentation"),
    path("presentations", PresentationDocumentListCreateAPIView.as_view(), name="presentation-documents"),
    path(
        "presentations/<uuid:document_id>",
        PresentationDocumentDetailAPIView.as_view(),
        name="presentation-document-detail",
    ),
]
