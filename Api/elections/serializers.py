from rest_framework import serializers
from .models import Election
from election_types.models import ElectionType


class ElectionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectionType
        fields = ['id', 'name', 'description']


class ElectionSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d/%m/%Y", read_only=True)
    updated_at = serializers.DateTimeField(format="%d/%m/%Y", read_only=True)
    type_name = serializers.CharField(source='type.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    progress_percentage_display = serializers.CharField(source='get_progress_percentage_display', read_only=True)

    # Format de date jj/mm/aaaa
    date = serializers.DateField(format="%d/%m/%Y", input_formats=["%d/%m/%Y", "%d/%m/%y"])

    class Meta:
        model = Election
        fields = [
            'id', 'title', 'type', 'type_name', 'date', 'status',
            'status_display', 'candidates_count', 'progress_percentage', 
            'progress_percentage_display', 'description', 'is_active', 
            'created_at', 'updated_at'
        ]

    def validate_candidates_count(self, value):
        """
        Validation personnalisée pour candidates_count
        """
        if value is not None and value <= 0:
            raise serializers.ValidationError("Le nombre de candidats doit être supérieur à zéro.")
        return value

    def validate_progress_percentage(self, value):
        """Validation personnalisée pour progress_percentage"""
        if value is not None:
            allowed_values = [25.00, 50.00, 75.00, 100.00]
            if value not in allowed_values:
                raise serializers.ValidationError(
                    "Le pourcentage de progression doit être 25, 50, 75 ou 100."
                )
        return value

    def validate(self, data):
        election_type = data.get('type')
        date = data.get('date')

        if election_type and date:
            # Vérifier s'il existe déjà une élection du même type la même année
            qs = Election.objects.filter(
                type=election_type,
                date__year=date.year
            )
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError(
                    {"type": f"Il existe déjà une élection de type '{election_type}' pour l'année {date.year}."}
                )
                
        return data