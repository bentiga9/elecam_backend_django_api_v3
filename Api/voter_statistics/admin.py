from django.contrib import admin
from .models import VoterStatistics


@admin.register(VoterStatistics)
class VoterStatisticsAdmin(admin.ModelAdmin):
    """Admin pour les statistiques électorales globales."""
    
    list_display = [
        'election',
        'total_inscrits',
        'total_votants',
        'taux_participation',
        'total_suffrages_exprimes',
        'created_at',
    ]
    list_filter = ['election__type', 'created_at']
    search_fields = ['election__title']
    readonly_fields = ['created_at', 'updated_at']