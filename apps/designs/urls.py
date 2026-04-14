from django.urls import path

from apps.designs.views import (
    DesignDocumentDetailAPIView,
    DesignDocumentListCreateAPIView,
    DesignDocumentRestoreVersionAPIView,
    DesignDocumentVersionsAPIView,
)


urlpatterns = [
    path("documents", DesignDocumentListCreateAPIView.as_view(), name="design-documents"),
    path(
        "documents/<uuid:document_id>",
        DesignDocumentDetailAPIView.as_view(),
        name="design-document-detail",
    ),
    path(
        "documents/<uuid:document_id>/versions",
        DesignDocumentVersionsAPIView.as_view(),
        name="design-document-versions",
    ),
    path(
        "documents/<uuid:document_id>/restore",
        DesignDocumentRestoreVersionAPIView.as_view(),
        name="design-document-restore",
    ),
]
