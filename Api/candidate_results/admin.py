from django.contrib import admin
from .models import CandidateRegionResult, CandidateDepartmentResult, CandidateGlobalResult, CandidateDiasporaResult


@admin.register(CandidateGlobalResult)
class CandidateGlobalResultAdmin(admin.ModelAdmin):
    list_display = (
        'rang',
        'candidate',
        'election',
        'total_suffrages',
        'pourcentage_national',
        'is_winner'
    )
    list_filter = ('election', 'is_winner')
    search_fields = ('candidate__name',)
    ordering = ('election', 'rang')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(CandidateRegionResult)
class CandidateRegionResultAdmin(admin.ModelAdmin):
    list_display = (
        'candidate',
        'region',
        'election',
        'suffrages',
        'pourcentage'
    )
    list_filter = ('election', 'region')
    search_fields = ('candidate__name', 'region__name')
    ordering = ('election', 'region', '-pourcentage')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(CandidateDepartmentResult)
class CandidateDepartmentResultAdmin(admin.ModelAdmin):
    list_display = (
        'candidate',
        'department',
        'election',
        'suffrages',
        'pourcentage'
    )
    list_filter = ('election', 'department__region')
    search_fields = ('candidate__name', 'department__name')
    ordering = ('election', 'department__region', 'department', '-pourcentage')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(CandidateDiasporaResult)
class CandidateDiasporaResultAdmin(admin.ModelAdmin):
    list_display = (
        'candidate',
        'election',
        'total_suffrages_diaspora',
        'pourcentage_diaspora',
        'suffrages_afrique',
        'suffrages_amerique',
        'suffrages_asie',
        'suffrages_europe'
    )
    list_filter = ('election',)
    search_fields = ('candidate__name', 'candidate__partie_politique__name')
    ordering = ('election', '-pourcentage_diaspora')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('election', 'candidate')
        }),
        ('Résultats agrégés', {
            'fields': ('total_suffrages_diaspora', 'pourcentage_diaspora')
        }),
        ('Détails par zone diaspora', {
            'fields': ('suffrages_afrique', 'suffrages_amerique', 'suffrages_asie', 'suffrages_europe')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
