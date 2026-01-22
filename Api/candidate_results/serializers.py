from rest_framework import serializers
from .models import CandidateRegionResult, CandidateDepartmentResult, CandidateGlobalResult, CandidateDiasporaResult


class CandidateGlobalResultSerializer(serializers.ModelSerializer):
    candidate_name = serializers.CharField(source='candidate.name', read_only=True)
    party_name = serializers.CharField(source='candidate.partie_politique.name', read_only=True)
    party_abbreviation = serializers.CharField(source='candidate.partie_politique.abbreviation', read_only=True)
    election_title = serializers.CharField(source='election.title', read_only=True)
    
    class Meta:
        model = CandidateGlobalResult
        fields = [
            'id',
            'election',
            'election_title',
            'candidate',
            'candidate_name',
            'party_name',
            'party_abbreviation',
            'rang',
            'total_suffrages',
            'pourcentage_national',
            'is_winner',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class CandidateRegionResultSerializer(serializers.ModelSerializer):
    candidate_name = serializers.CharField(source='candidate.name', read_only=True)
    region_name = serializers.CharField(source='region.name', read_only=True)
    party_abbreviation = serializers.CharField(source='candidate.partie_politique.abbreviation', read_only=True)
    
    class Meta:
        model = CandidateRegionResult
        fields = [
            'id',
            'election',
            'candidate',
            'candidate_name',
            'party_abbreviation',
            'region',
            'region_name',
            'suffrages',
            'pourcentage',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class CandidateDepartmentResultSerializer(serializers.ModelSerializer):
    candidate_name = serializers.CharField(source='candidate.name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    region_name = serializers.CharField(source='department.region.name', read_only=True)
    party_abbreviation = serializers.CharField(source='candidate.partie_politique.abbreviation', read_only=True)
    
    class Meta:
        model = CandidateDepartmentResult
        fields = [
            'id',
            'election',
            'candidate',
            'candidate_name',
            'party_abbreviation',
            'department',
            'department_name',
            'region_name',
            'suffrages',
            'pourcentage',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class CandidateDiasporaResultSerializer(serializers.ModelSerializer):
    candidate_name = serializers.CharField(source='candidate.name', read_only=True)
    party_name = serializers.CharField(source='candidate.partie_politique.name', read_only=True)
    party_abbreviation = serializers.CharField(source='candidate.partie_politique.abbreviation', read_only=True)
    election_title = serializers.CharField(source='election.title', read_only=True)
    
    class Meta:
        model = CandidateDiasporaResult
        fields = [
            'id',
            'election',
            'election_title',
            'candidate',
            'candidate_name',
            'party_name',
            'party_abbreviation',
            'total_suffrages_diaspora',
            'pourcentage_diaspora',
            'suffrages_afrique',
            'suffrages_amerique',
            'suffrages_asie',
            'suffrages_europe',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class CandidateResultSummarySerializer(serializers.Serializer):
    """Serializer pour le résumé des résultats d'un candidat"""
    candidate_id = serializers.IntegerField()
    candidate_name = serializers.CharField()
    party_name = serializers.CharField()
    party_abbreviation = serializers.CharField()
    rang = serializers.IntegerField()
    total_suffrages = serializers.IntegerField()
    pourcentage_national = serializers.DecimalField(max_digits=5, decimal_places=2)
    is_winner = serializers.BooleanField()
    region_results = CandidateRegionResultSerializer(many=True)
