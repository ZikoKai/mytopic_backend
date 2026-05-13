from django.urls import path

from apps.ai.views import (
    AIProviderConfigDetailAPIView,
    AIProviderConfigListCreateAPIView,
    AIProviderSetDefaultAPIView,
    AIProviderTestConnectionAPIView,
)


urlpatterns = [
    path("providers", AIProviderConfigListCreateAPIView.as_view(), name="ai-provider-configs"),
    path("providers/<int:provider_id>", AIProviderConfigDetailAPIView.as_view(), name="ai-provider-config-detail"),
    path(
        "providers/<int:provider_id>/test",
        AIProviderTestConnectionAPIView.as_view(),
        name="ai-provider-test-connection",
    ),
    path(
        "providers/<int:provider_id>/default",
        AIProviderSetDefaultAPIView.as_view(),
        name="ai-provider-set-default",
    ),
]
