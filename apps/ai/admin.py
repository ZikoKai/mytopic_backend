from django.contrib import admin

from apps.ai.models import AIProviderConfig


@admin.register(AIProviderConfig)
class AIProviderConfigAdmin(admin.ModelAdmin):
    list_display = (
        "provider_name",
        "owner",
        "provider_type",
        "model_name",
        "is_default",
        "is_active",
        "updated_at",
    )
    list_filter = ("provider_type", "is_default", "is_active")
    search_fields = ("provider_name", "model_name", "owner__username", "owner__email")
    readonly_fields = ("encrypted_api_key", "created_at", "updated_at")
