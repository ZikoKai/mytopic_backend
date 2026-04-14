from rest_framework import serializers

from apps.designs.models import DesignDocument, DesignDocumentVersion


class DesignDocumentVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignDocumentVersion
        fields = ["id", "version_number", "created_at", "created_by_id"]


class DesignDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignDocument
        fields = [
            "id",
            "title",
            "content",
            "current_version",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "current_version", "created_at", "updated_at"]


class DesignDocumentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignDocument
        fields = ["id", "title", "current_version", "updated_at", "created_at"]


class DesignDocumentSaveSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=1, max_length=255)
    content = serializers.JSONField()
    create_version = serializers.BooleanField(required=False, default=True)


class RestoreVersionSerializer(serializers.Serializer):
    version_number = serializers.IntegerField(min_value=1)
