from rest_framework import serializers
from .models import DiasporaStat


class DiasporaStatSerializer(serializers.ModelSerializer):
    election_title = serializers.CharField(source='election.title', read_only=True)
    zone_display = serializers.CharField(source='get_zone_display', read_only=True)
    
    class Meta:
        model = DiasporaStat
        fields = [
            'id',
            'election',
            'election_title',
            'zone',
            'zone_display',
            'inscrits',
            'votants',
            'taux_participation',
            'taux_abstention',
            'bulletins_nuls',
            'suffrages_exprimes',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class DiasporaStatListSerializer(serializers.ModelSerializer):
    """Serializer léger pour les listes"""
    zone_display = serializers.CharField(source='get_zone_display', read_only=True)
    
    class Meta:
        model = DiasporaStat
        fields = [
            'id',
            'zone',
            'zone_display',
            'inscrits',
            'votants',
            'taux_participation',
            'suffrages_exprimes'
        ]
