import logging

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.ai.models import AIProviderConfig
from apps.ai.orchestrator import AIService
from apps.ai.serializers import AIProviderConfigSerializer

logger = logging.getLogger(__name__)


class AIProviderConfigListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: object) -> Response:
        queryset = AIProviderConfig.objects.filter(owner=request.user)
        serializer = AIProviderConfigSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: object) -> Response:
        serializer = AIProviderConfigSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        config = serializer.save()
        logger.info(
            "AI provider config created user_id=%s provider_id=%s type=%s",
            request.user.id,
            config.id,
            config.provider_type,
        )
        return Response(AIProviderConfigSerializer(config).data, status=status.HTTP_201_CREATED)


class AIProviderConfigDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, request: object, provider_id: int) -> AIProviderConfig:
        return get_object_or_404(
            AIProviderConfig,
            id=provider_id,
            owner=request.user,
        )

    def put(self, request: object, provider_id: int) -> Response:
        config = self.get_object(request, provider_id)
        serializer = AIProviderConfigSerializer(
            config,
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        updated = serializer.save()
        logger.info(
            "AI provider config updated user_id=%s provider_id=%s type=%s",
            request.user.id,
            updated.id,
            updated.provider_type,
        )
        return Response(AIProviderConfigSerializer(updated).data, status=status.HTTP_200_OK)

    def patch(self, request: object, provider_id: int) -> Response:
        config = self.get_object(request, provider_id)
        serializer = AIProviderConfigSerializer(
            config,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        updated = serializer.save()
        return Response(AIProviderConfigSerializer(updated).data, status=status.HTTP_200_OK)

    def delete(self, request: object, provider_id: int) -> Response:
        config = self.get_object(request, provider_id)
        logger.info(
            "AI provider config deleted user_id=%s provider_id=%s type=%s",
            request.user.id,
            config.id,
            config.provider_type,
        )
        config.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AIProviderTestConnectionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: object, provider_id: int) -> Response:
        config = get_object_or_404(
            AIProviderConfig,
            id=provider_id,
            owner=request.user,
        )
        result = AIService(user=request.user).test_provider(config)
        config.last_error = "" if result.ok else result.message[:500]
        config.save(update_fields=["last_error", "updated_at"])
        logger.info(
            "AI provider connection tested user_id=%s provider_id=%s ok=%s",
            request.user.id,
            config.id,
            result.ok,
        )
        return Response(
            {
                "ok": result.ok,
                "message": result.message,
                "details": result.details,
            },
            status=status.HTTP_200_OK if result.ok else status.HTTP_400_BAD_REQUEST,
        )


class AIProviderSetDefaultAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: object, provider_id: int) -> Response:
        config = get_object_or_404(
            AIProviderConfig,
            id=provider_id,
            owner=request.user,
        )
        config.is_default = True
        config.is_active = True
        config.save(update_fields=["is_default", "is_active", "updated_at"])
        logger.info(
            "AI provider set as default user_id=%s provider_id=%s type=%s",
            request.user.id,
            config.id,
            config.provider_type,
        )
        return Response(AIProviderConfigSerializer(config).data, status=status.HTTP_200_OK)
