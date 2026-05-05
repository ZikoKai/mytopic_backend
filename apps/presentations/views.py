from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.presentations.models import PresentationDocument
from apps.presentations.serializers import (
    FavoriteImageAssetSaveSerializer,
    FavoriteImageAssetSerializer,
    GenerateImageRequestSerializer,
    GenerateRequestSerializer,
    PresentationDocumentListSerializer,
    PresentationDocumentSaveSerializer,
    PresentationDocumentSerializer,
)
from apps.presentations.services import (
    AIClientError,
    generate_image_for_presentation,
    generate_topic_presentation,
)


class GeneratePresentationAPIView(APIView):
    """
    Endpoint DRF de generation de presentation.

    Securite:
    - Valide le payload et masque les erreurs internes provider.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request: object) -> Response:
        """
        Genere une presentation JSON depuis un sujet.

        @param request Requete HTTP DRF.
        @returns Reponse JSON de presentation ou erreur.
        Securite:
        - Retourne des erreurs normalisees sans stacktrace interne.
        """
        serializer = GenerateRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data

        try:
            data = generate_topic_presentation(
                topic=payload["topic"],
                language=payload.get("language") or None,
            )
        except AIClientError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_502_BAD_GATEWAY)

        return Response(data, status=status.HTTP_200_OK)


class GeneratePresentationImageAPIView(APIView):
    """
    Endpoint DRF de generation d'image depuis un prompt texte.

    Securite:
    - Valide le payload.
    - Normalise les erreurs provider.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request: object) -> Response:
        serializer = GenerateImageRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data

        try:
            image = generate_image_for_presentation(
                prompt=payload["prompt"],
                size=payload.get("size", "1024x1024"),
            )
        except AIClientError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_502_BAD_GATEWAY)

        return Response(image, status=status.HTTP_200_OK)


class PresentationDocumentListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: object) -> Response:
        queryset = PresentationDocument.objects.filter(owner=request.user)
        serializer = PresentationDocumentListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: object) -> Response:
        serializer = PresentationDocumentSaveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data

        document = PresentationDocument.objects.create(
            owner=request.user,
            title=payload["title"],
            content=payload["content"],
        )
        out = PresentationDocumentSerializer(document)
        return Response(out.data, status=status.HTTP_201_CREATED)


class PresentationDocumentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, request: object, document_id: str) -> PresentationDocument:
        return get_object_or_404(
            PresentationDocument,
            id=document_id,
            owner=request.user,
        )

    def get(self, request: object, document_id: str) -> Response:
        document = self.get_object(request, document_id)
        serializer = PresentationDocumentSerializer(document)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: object, document_id: str) -> Response:
        document = self.get_object(request, document_id)
        serializer = PresentationDocumentSaveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data

        document.title = payload["title"]
        document.content = payload["content"]
        document.save(update_fields=["title", "content", "updated_at"])
        out = PresentationDocumentSerializer(document)
        return Response(out.data, status=status.HTTP_200_OK)

    def delete(self, request: object, document_id: str) -> Response:
        document = self.get_object(request, document_id)
        document.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteImageAssetListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: object) -> Response:
        queryset = request.user.favorite_image_assets.all()
        serializer = FavoriteImageAssetSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: object) -> Response:
        serializer = FavoriteImageAssetSaveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data

        document = request.user.favorite_image_assets.create(
            title=payload.get("title", ""),
            prompt=payload.get("prompt", ""),
            image_data_url=payload["image_data_url"],
            mime_type=payload.get("mime_type", "image/png") or "image/png",
        )
        out = FavoriteImageAssetSerializer(document)
        return Response(out.data, status=status.HTTP_201_CREATED)


class FavoriteImageAssetDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request: object, asset_id: str) -> Response:
        asset = get_object_or_404(
            request.user.favorite_image_assets,
            id=asset_id,
        )
        asset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
