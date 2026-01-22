from rest_framework import serializers
from .models import Region


class RegionSerializer(serializers.ModelSerializer):
    is_diaspora = serializers.BooleanField(read_only=True)
    departments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Region
        fields = [
            'id', 
            'name', 
            'code', 
            'region_type',
            'chef_lieu',
            'is_diaspora',
            'is_active',
            'departments_count',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_departments_count(self, obj):
        return obj.departments.count() if hasattr(obj, 'departments') else 0


class RegionListSerializer(serializers.ModelSerializer):
    """Serializer léger pour les listes"""
    class Meta:
        model = Region
        fields = ['id', 'name', 'code', 'region_type']