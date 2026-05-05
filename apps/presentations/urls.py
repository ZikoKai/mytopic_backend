from django.urls import path

from apps.presentations.views import (
    FavoriteImageAssetDetailAPIView,
    FavoriteImageAssetListCreateAPIView,
    GeneratePresentationImageAPIView,
    GeneratePresentationAPIView,
    PresentationDocumentDetailAPIView,
    PresentationDocumentListCreateAPIView,
)


urlpatterns = [
    path("presentations/generate", GeneratePresentationAPIView.as_view(), name="generate-presentation"),
    path(
        "presentations/generate-image",
        GeneratePresentationImageAPIView.as_view(),
        name="generate-presentation-image",
    ),
    path("presentations", PresentationDocumentListCreateAPIView.as_view(), name="presentation-documents"),
    path(
        "presentations/uploads",
        FavoriteImageAssetListCreateAPIView.as_view(),
        name="favorite-image-assets",
    ),
    path(
        "presentations/uploads/<uuid:asset_id>",
        FavoriteImageAssetDetailAPIView.as_view(),
        name="favorite-image-asset-detail",
    ),
    path(
        "presentations/<uuid:document_id>",
        PresentationDocumentDetailAPIView.as_view(),
        name="presentation-document-detail",
    ),
]
