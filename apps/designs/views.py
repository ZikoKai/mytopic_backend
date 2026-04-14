from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.designs.models import DesignDocument, DesignDocumentVersion
from apps.designs.serializers import (
    DesignDocumentListSerializer,
    DesignDocumentSaveSerializer,
    DesignDocumentSerializer,
    DesignDocumentVersionSerializer,
    RestoreVersionSerializer,
)


class DesignDocumentListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: object) -> Response:
        queryset = DesignDocument.objects.filter(owner=request.user)
        serializer = DesignDocumentListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request: object) -> Response:
        serializer = DesignDocumentSaveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data

        document = DesignDocument.objects.create(
            owner=request.user,
            title=payload["title"],
            content=payload["content"],
            current_version=1,
        )
        DesignDocumentVersion.objects.create(
            document=document,
            version_number=1,
            content=payload["content"],
            created_by=request.user,
        )
        out = DesignDocumentSerializer(document)
        return Response(out.data, status=status.HTTP_201_CREATED)


class DesignDocumentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, request: object, document_id: str) -> DesignDocument:
        return get_object_or_404(
            DesignDocument,
            id=document_id,
            owner=request.user,
        )

    def get(self, request: object, document_id: str) -> Response:
        document = self.get_object(request, document_id)
        serializer = DesignDocumentSerializer(document)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def put(self, request: object, document_id: str) -> Response:
        document = self.get_object(request, document_id)
        serializer = DesignDocumentSaveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data

        document.title = payload["title"]
        document.content = payload["content"]
        create_version = payload.get("create_version", True)
        if create_version:
            document.current_version += 1
            DesignDocumentVersion.objects.create(
                document=document,
                version_number=document.current_version,
                content=document.content,
                created_by=request.user,
            )
        document.save(update_fields=["title", "content", "current_version", "updated_at"])
        out = DesignDocumentSerializer(document)
        return Response(out.data, status=status.HTTP_200_OK)

    def delete(self, request: object, document_id: str) -> Response:
        document = self.get_object(request, document_id)
        document.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DesignDocumentVersionsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: object, document_id: str) -> Response:
        document = get_object_or_404(
            DesignDocument,
            id=document_id,
            owner=request.user,
        )
        serializer = DesignDocumentVersionSerializer(document.versions.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DesignDocumentRestoreVersionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request: object, document_id: str) -> Response:
        document = get_object_or_404(
            DesignDocument,
            id=document_id,
            owner=request.user,
        )
        serializer = RestoreVersionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        version_number = serializer.validated_data["version_number"]

        version = get_object_or_404(
            DesignDocumentVersion,
            document=document,
            version_number=version_number,
        )

        document.content = version.content
        document.current_version += 1
        document.save(update_fields=["content", "current_version", "updated_at"])
        DesignDocumentVersion.objects.create(
            document=document,
            version_number=document.current_version,
            content=document.content,
            created_by=request.user,
        )
        out = DesignDocumentSerializer(document)
        return Response(out.data, status=status.HTTP_200_OK)
