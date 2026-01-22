from django.contrib import admin
from .models import Region


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    """
    Admin personnalisé pour le modèle Region.
    """
    # Champs affichés dans la liste
    list_display = [
        'name',
        'code',
    ]

    # Champs recherchables
    search_fields = ['name', 'code']