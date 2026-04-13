from rest_framework.response import Response
from rest_framework.views import APIView


class UsersHealthAPIView(APIView):
    """Simple placeholder view for users app."""

    def get(self, _: object) -> Response:
        return Response({"status": "users-app-ready"})
