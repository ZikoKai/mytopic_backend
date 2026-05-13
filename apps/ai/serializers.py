from rest_framework import serializers

from apps.ai.models import AIProviderConfig
from apps.ai.types import ProviderType


class AIProviderConfigSerializer(serializers.ModelSerializer):
    apiKey = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
        max_length=4000,
    )
    hasApiKey = serializers.BooleanField(source="has_api_key", read_only=True)
    providerName = serializers.CharField(source="provider_name", max_length=120)
    providerType = serializers.ChoiceField(
        source="provider_type",
        choices=[item.value for item in ProviderType],
    )
    baseUrl = serializers.URLField(
        source="base_url",
        required=False,
        allow_blank=True,
        max_length=500,
    )
    modelName = serializers.CharField(source="model_name", max_length=160)
    maxTokens = serializers.IntegerField(source="max_tokens", min_value=1, max_value=50000)
    timeoutMs = serializers.IntegerField(source="timeout_ms", min_value=1000, max_value=600000)
    isDefault = serializers.BooleanField(source="is_default", required=False)
    isActive = serializers.BooleanField(source="is_active", required=False)
    lastError = serializers.CharField(source="last_error", read_only=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)

    class Meta:
        model = AIProviderConfig
        fields = [
            "id",
            "providerName",
            "providerType",
            "baseUrl",
            "apiKey",
            "hasApiKey",
            "modelName",
            "temperature",
            "maxTokens",
            "timeoutMs",
            "isDefault",
            "isActive",
            "lastError",
            "createdAt",
            "updatedAt",
        ]

    def validate(self, attrs: dict) -> dict:
        provider_type = attrs.get("provider_type") or getattr(self.instance, "provider_type", "")
        base_url = attrs.get("base_url") or getattr(self.instance, "base_url", "")

        if provider_type in {ProviderType.OLLAMA.value, ProviderType.OPENAI_COMPATIBLE.value, ProviderType.CUSTOM.value} and not base_url:
            raise serializers.ValidationError({"baseUrl": "baseUrl is required for this provider type."})

        temperature = attrs.get("temperature")
        if temperature is not None and not 0 <= temperature <= 2:
            raise serializers.ValidationError({"temperature": "temperature must be between 0 and 2."})

        return attrs

    def create(self, validated_data: dict) -> AIProviderConfig:
        api_key = validated_data.pop("apiKey", "")
        config = AIProviderConfig(**validated_data)
        config.owner = self.context["request"].user
        if api_key:
            config.set_api_key(api_key)
        config.save()
        return config

    def update(self, instance: AIProviderConfig, validated_data: dict) -> AIProviderConfig:
        api_key = validated_data.pop("apiKey", None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        if api_key is not None and api_key.strip():
            instance.set_api_key(api_key)
        instance.save()
        return instance


class ConnectionResultSerializer(serializers.Serializer):
    ok = serializers.BooleanField()
    message = serializers.CharField()
    details = serializers.JSONField(required=False, allow_null=True)
