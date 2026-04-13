from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    """Minimal user serializer scaffold."""

    id = serializers.IntegerField()
    username = serializers.CharField()
