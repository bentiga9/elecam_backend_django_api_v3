from rest_framework import serializers
from .models import Department
from regions.serializers import RegionSerializer


class DepartmentSerializer(serializers.ModelSerializer):
    region_detail = RegionSerializer(source='region', read_only=True)
    
    class Meta:
        model = Department
        fields = [
            'id', 
            'name', 
            'code', 
            'region', 
            'region_detail',
            'chef_lieu',
            'created_at', 
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class DepartmentListSerializer(serializers.ModelSerializer):
    """Serializer léger pour les listes"""
    region_name = serializers.CharField(source='region.name', read_only=True)
    
    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'region', 'region_name']
