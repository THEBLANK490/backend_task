from rest_framework import serializers

from app.users.models import User


class GeoJsonSerializer(serializers.Serializer):
    """
    Serializer for the GeoJsonView.
    """

    type = serializers.CharField()
    geometry = serializers.JSONField()
    properties = serializers.DictField()


class NerbyUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the NearbyUsersView and uses the model User.
    """

    class Meta:
        model = User
        fields = ["id", "username", "home_address", "office_address"]
