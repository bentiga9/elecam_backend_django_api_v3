from rest_framework import serializers
from .models import CalendrierElectoral
from election_types.serializers import ElectionTypeSerializer


class CalendrierElectoralSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle CalendrierElectoral
    """
    type_election_detail = ElectionTypeSerializer(source='type_election', read_only=True)
    is_past = serializers.ReadOnlyField()
    is_today = serializers.ReadOnlyField()
    is_upcoming = serializers.ReadOnlyField()
    is_recent = serializers.ReadOnlyField()
    days_until_election = serializers.ReadOnlyField()
    status_color = serializers.ReadOnlyField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = CalendrierElectoral
        fields = [
            'id',
            'type_election',
            'type_election_detail',
            'date',
            'status',
            'status_display',
            'status_color',
            'is_past',
            'is_today',
            'is_upcoming',
            'days_until_election',
            'is_recent',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
            'type_election_detail',
            'is_past',
            'is_today',
            'is_upcoming',
            'days_until_election',
            'is_recent',
            'status_color',
            'status_display'
        ]

    def validate_date(self, value):
        """Validation de la date"""
        from django.utils import timezone

        # Pour les nouvelles créations, vérifier que la date n'est pas dans le passé
        if not self.instance and value < timezone.now():
            raise serializers.ValidationError("La date de l'élection ne peut pas être dans le passé.")

        return value


class CalendrierElectoralCreateSerializer(serializers.ModelSerializer):
    """
    Serializer spécialisé pour la création de calendriers électoraux
    """

    class Meta:
        model = CalendrierElectoral
        fields = [
            'type_election',
            'date',
            'status'
        ]

    def validate_date(self, value):
        """Validation de la date"""
        from django.utils import timezone

        if value < timezone.now():
            raise serializers.ValidationError("La date de l'élection ne peut pas être dans le passé.")

        return value


class CalendrierElectoralStatsSerializer(serializers.Serializer):
    """
    Serializer pour les statistiques du calendrier électoral
    """
    total_elections = serializers.IntegerField()
    elections_planifiees = serializers.IntegerField()
    elections_en_cours = serializers.IntegerField()
    elections_terminees = serializers.IntegerField()
    elections_reportees = serializers.IntegerField()
    elections_annulees = serializers.IntegerField()
    elections_today = serializers.IntegerField()
    elections_upcoming = serializers.IntegerField()
    elections_past = serializers.IntegerField()


class CalendrierElectoralUpcomingSerializer(serializers.ModelSerializer):
    """
    Serializer pour les élections à venir (format simplifié)
    """
    type_election_name = serializers.CharField(source='type_election.name', read_only=True)
    days_until = serializers.ReadOnlyField(source='days_until_election')
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = CalendrierElectoral
        fields = [
            'id',
            'type_election_name',
            'date',
            'status',
            'status_display',
            'days_until',
            'is_today'
        ]