from django.contrib import admin
from .models import Candidat

@admin.register(Candidat)
class CandidatAdmin(admin.ModelAdmin):
    list_display = ('name', 'election', 'partie_politique', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('election', 'partie_politique', 'created_at', 'updated_at')
    ordering = ('name',)