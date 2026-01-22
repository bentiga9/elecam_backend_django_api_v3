from rest_framework import serializers
from .models import RegionStat
from regions.serializers import RegionSerializer


class RegionStatSerializer(serializers.ModelSerializer):
    region_detail = RegionSerializer(source='region', read_only=True)
    election_title = serializers.CharField(source='election.title', read_only=True)
    region_name = serializers.CharField(source='region.name', read_only=True)
    region_type = serializers.CharField(source='region.region_type', read_only=True)
    
    class Meta:
        model = RegionStat
        fields = [
            'id',
            'election',
            'election_title',
            'region',
            'region_detail',
            'region_name',
            'region_type',
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


class RegionStatListSerializer(serializers.ModelSerializer):
    """Serializer léger pour les listes de statistiques régionales"""
    region_name = serializers.CharField(source='region.name', read_only=True)
    region_code = serializers.CharField(source='region.code', read_only=True)
    region_type = serializers.CharField(source='region.region_type', read_only=True)
    
    class Meta:
        model = RegionStat
        fields = [
            'id',
            'region',
            'region_name',
            'region_code',
            'region_type',
            'inscrits',
            'votants',
            'taux_participation',
            'suffrages_exprimes'
        ]


class RegionStatAggregateSerializer(serializers.Serializer):
    """Serializer pour les statistiques agrégées par région"""
    region_name = serializers.CharField()
    region_code = serializers.CharField()
    total_inscrits = serializers.IntegerField()
    total_votants = serializers.IntegerField()
    taux_participation_moyen = serializers.DecimalField(max_digits=5, decimal_places=2)
    total_bulletins_nuls = serializers.IntegerField()
    total_suffrages_exprimes = serializers.IntegerField()
    nombre_departements = serializers.IntegerField()
