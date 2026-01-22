from django.contrib import admin
from .models import DepartmentStat


@admin.register(DepartmentStat)
class DepartmentStatAdmin(admin.ModelAdmin):
    list_display = (
        'department', 
        'election', 
        'inscrits', 
        'votants', 
        'taux_participation',
        'bulletins_nuls',
        'suffrages_exprimes'
    )
    list_filter = ('election', 'department__region')
    search_fields = ('department__name', 'election__title')
    ordering = ('election', 'department__region', 'department')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Identifiant', {
            'fields': ('election', 'department')
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
