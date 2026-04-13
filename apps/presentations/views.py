from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.presentations.serializers import GenerateRequestSerializer
from apps.presentations.services import AIClientError, generate_topic_presentation


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
