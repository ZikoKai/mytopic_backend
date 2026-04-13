from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class SlidesHealthAPIView(APIView):
    """Simple placeholder endpoint for slides app."""

    permission_classes = [IsAuthenticated]

    def get(self, _: object) -> Response:
        return Response({"status": "slides-app-ready"})
