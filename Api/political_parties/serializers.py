from rest_framework import serializers
from .models import PartiePolitique

class PartiePolitiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartiePolitique
        fields = ['id', 'name', 'abbreviation', 'logo_url', 'color_hex', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']