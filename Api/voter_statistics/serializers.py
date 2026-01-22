from rest_framework import serializers
from .models import VoterStatistics


class VoterStatisticsSerializer(serializers.ModelSerializer):
    election_title = serializers.CharField(source='election.title', read_only=True)
    election_date = serializers.DateField(source='election.date', read_only=True)

    class Meta:
        model = VoterStatistics
        fields = [
            'id', 
            'election',
            'election_title',
            'election_date',
            'total_inscrits', 
            'total_votants', 
            'taux_participation',
            'taux_abstention',
            'total_bulletins_nuls',
            'total_suffrages_exprimes',
            'inscrits_cameroun',
            'votants_cameroun',
            'inscrits_diaspora',
            'votants_diaspora',
            'created_at', 
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class VoterStatisticsSummarySerializer(serializers.ModelSerializer):
    """Serializer résumé pour affichage rapide"""
    election_title = serializers.CharField(source='election.title', read_only=True)
    
    class Meta:
        model = VoterStatistics
        fields = [
            'id',
            'election',
            'election_title',
            'total_inscrits',
            'total_votants',
            'taux_participation',
            'total_suffrages_exprimes'
        ]