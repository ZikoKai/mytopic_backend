from rest_framework import serializers


class GenerateRequestSerializer(serializers.Serializer):
    """
    Serializer d'entree pour la generation de presentation.

    Securite:
    - Valide les champs d'entree avant appel AI.
    """

    topic = serializers.CharField(min_length=1, max_length=500)
    language = serializers.CharField(required=False, allow_null=True, allow_blank=True)
