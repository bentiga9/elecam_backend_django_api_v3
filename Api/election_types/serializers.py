from rest_framework import serializers
from .models import ElectionType


class ElectionTypeSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d/%m/%Y", read_only=True)
    updated_at = serializers.DateTimeField(format="%d/%m/%Y", read_only=True)
    
    class Meta:
        model = ElectionType
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']