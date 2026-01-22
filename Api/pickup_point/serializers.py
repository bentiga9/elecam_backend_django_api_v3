from rest_framework import serializers
from .models import PickupPoint


class PickupPointSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle PickupPoint
    """
    coordinates = serializers.ReadOnlyField()
    is_recent = serializers.ReadOnlyField()

    class Meta:
        model = PickupPoint
        fields = [
            'id',
            'name',
            'description',
            'nombre',
            'latitude',
            'longitude',
            'type',
            'coordinates',
            'is_recent',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'coordinates', 'is_recent']

    def validate_latitude(self, value):
        """Validation de la latitude"""
        if value < 0:
            raise serializers.ValidationError("La latitude ne peut pas être négative.")
        if value > 90:
            raise serializers.ValidationError("La latitude ne peut pas dépasser 90 degrés.")
        return value

    def validate_longitude(self, value):
        """Validation de la longitude"""
        if value < 0:
            raise serializers.ValidationError("La longitude ne peut pas être négative.")
        if value > 180:
            raise serializers.ValidationError("La longitude ne peut pas dépasser 180 degrés.")
        return value


class PickupPointCreateSerializer(serializers.ModelSerializer):
    """
    Serializer spécialisé pour la création de points de retrait
    """

    class Meta:
        model = PickupPoint
        fields = [
            'name',
            'description',
            'nombre',
            'latitude',
            'longitude',
            'type'
        ]

    def validate_latitude(self, value):
        """Validation de la latitude"""
        if value < 0:
            raise serializers.ValidationError("La latitude ne peut pas être négative.")
        if value > 90:
            raise serializers.ValidationError("La latitude ne peut pas dépasser 90 degrés.")
        return value

    def validate_longitude(self, value):
        """Validation de la longitude"""
        if value < 0:
            raise serializers.ValidationError("La longitude ne peut pas être négative.")
        if value > 180:
            raise serializers.ValidationError("La longitude ne peut pas dépasser 180 degrés.")
        return value


class PickupPointLocationSerializer(serializers.Serializer):
    """
    Serializer pour les données de localisation
    """
    latitude = serializers.DecimalField(max_digits=10, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=10, decimal_places=6)
    name = serializers.CharField(max_length=255)
    type = serializers.CharField(max_length=50)