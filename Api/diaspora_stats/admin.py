from django.contrib import admin
from .models import DiasporaStat


@admin.register(DiasporaStat)
class DiasporaStatAdmin(admin.ModelAdmin):
    list_display = (
        'zone',
        'election', 
        'inscrits', 
        'votants', 
        'taux_participation',
        'bulletins_nuls',
        'suffrages_exprimes'
    )
    list_filter = ('election', 'zone')
    search_fields = ('zone', 'election__title')
    ordering = ('election', 'zone')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Identifiant', {
            'fields': ('election', 'zone')
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
