from django.contrib import admin
from .models import RegionStat


@admin.register(RegionStat)
class RegionStatAdmin(admin.ModelAdmin):
    list_display = (
        'region',
        'election', 
        'inscrits', 
        'votants', 
        'taux_participation',
        'bulletins_nuls',
        'suffrages_exprimes'
    )
    list_filter = ('election', 'region__region_type', 'region')
    search_fields = ('region__name', 'election__title')
    ordering = ('election', 'region__region_type', 'region')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Identifiant', {
            'fields': ('election', 'region')
        }),
        ('Participation', {
            'fields': ('inscrits', 'votants', 'taux_participation', 'taux_abstention')
        }),
        ('Bulletins', {
            'fields': ('bulletins_nuls', 'suffrages_exprimes')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
