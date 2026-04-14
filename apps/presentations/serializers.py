from rest_framework import serializers

from apps.presentations.models import PresentationDocument
from apps.presentations.validators import validate_presentation_content


class GenerateRequestSerializer(serializers.Serializer):
    """
    Serializer d'entree pour la generation de presentation.

    Securite:
    - Valide les champs d'entree avant appel AI.
    """

    topic = serializers.CharField(min_length=1, max_length=500)
    language = serializers.CharField(required=False, allow_null=True, allow_blank=True)


class PresentationDocumentSaveSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=1, max_length=255)
    content = serializers.JSONField()

    def validate_content(self, value: object) -> dict:
        try:
            return validate_presentation_content(value)
        except ValueError as exc:
            raise serializers.ValidationError(str(exc))


class PresentationDocumentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PresentationDocument
        fields = ["id", "title", "created_at", "updated_at"]


class PresentationDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PresentationDocument
        fields = ["id", "title", "content", "created_at", "updated_at"]
