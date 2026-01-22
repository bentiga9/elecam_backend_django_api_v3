from rest_framework import serializers
from .models import DepartmentStat
from departments.serializers import DepartmentListSerializer


class DepartmentStatSerializer(serializers.ModelSerializer):
    department_detail = DepartmentListSerializer(source='department', read_only=True)
    election_title = serializers.CharField(source='election.title', read_only=True)
    region_name = serializers.CharField(source='department.region.name', read_only=True)
    
    class Meta:
        model = DepartmentStat
        fields = [
            'id',
            'election',
            'election_title',
            'department',
            'department_detail',
            'region_name',
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


class DepartmentStatListSerializer(serializers.ModelSerializer):
    """Serializer léger pour les listes"""
    department_name = serializers.CharField(source='department.name', read_only=True)
    region_name = serializers.CharField(source='department.region.name', read_only=True)
    
    class Meta:
        model = DepartmentStat
        fields = [
            'id',
            'department',
            'department_name',
            'region_name',
            'inscrits',
            'votants',
            'taux_participation',
            'suffrages_exprimes'
        ]
