from rest_framework import serializers
from .models import Candidat
from political_parties.serializers import PartiePolitiqueSerializer


class CandidatSerializer(serializers.ModelSerializer):
    partie_politique_detail = PartiePolitiqueSerializer(source='partie_politique', read_only=True)
    election_title = serializers.CharField(source='election.title', read_only=True)
    
    class Meta:
        model = Candidat
        fields = [
            'id', 
            'election', 
            'election_title',
            'partie_politique', 
            'partie_politique_detail',
            'name',
            'is_active',
            'created_at', 
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CandidatListSerializer(serializers.ModelSerializer):
    """Serializer léger pour les listes"""
    party_name = serializers.CharField(source='partie_politique.name', read_only=True)
    party_abbreviation = serializers.CharField(source='partie_politique.abbreviation', read_only=True)
    
    class Meta:
        model = Candidat
        fields = [
            'id', 
            'name', 
            'party_name',
            'party_abbreviation',
        ]