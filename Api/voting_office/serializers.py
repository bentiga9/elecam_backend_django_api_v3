from rest_framework import serializers
from .models import VotingOffice


class VotingOfficeSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle VotingOffice
    """
    coordinates = serializers.ReadOnlyField()
    is_recent = serializers.ReadOnlyField()
    status_display = serializers.ReadOnlyField()

    class Meta:
        model = VotingOffice
        fields = [
            'id',
            'name',
            'description',
            'nombre',
            'latitude',
            'longitude',
            'is_active',
            'coordinates',
            'is_recent',
            'status_display',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'coordinates', 'is_recent', 'status_display']

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


class VotingOfficeCreateSerializer(serializers.ModelSerializer):
    """
    Serializer spécialisé pour la création de bureaux de vote
    """

    class Meta:
        model = VotingOffice
        fields = [
            'name',
            'description',
            'nombre',
            'latitude',
            'longitude',
            'is_active'
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


class VotingOfficeStatsSerializer(serializers.Serializer):
    """
    Serializer pour les statistiques des bureaux de vote
    """
    total_offices = serializers.IntegerField()
    active_offices = serializers.IntegerField()
    inactive_offices = serializers.IntegerField()
    recent_offices = serializers.IntegerField()
    activity_rate = serializers.DecimalField(max_digits=5, decimal_places=2)