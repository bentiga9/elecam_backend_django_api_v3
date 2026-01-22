from django.contrib import admin
from .models import ElectionType


@admin.register(ElectionType)
class ElectionTypeAdmin(admin.ModelAdmin):
    """
    Admin personnalisé pour le modèle ElectionType.
    """
    # Champs affichés dans la liste
    list_display = [
        'name',
        'description',
        'created_at',
        'updated_at',
    ]

    # Champs recherchables
    search_fields = ['name', 'description']
    
    # Champs en lecture seule
    readonly_fields = ['created_at', 'updated_at']