from django.contrib import admin
from django.utils.html import format_html
from .models import VotingOffice


@admin.register(VotingOffice)
class VotingOfficeAdmin(admin.ModelAdmin):
    """Configuration de l'interface d'administration pour VotingOffice"""

    # Champs affichés dans la liste
    list_display = [
        'id',
        'name',
        'nombre',
        'clickable_coordinates',
        'is_active',
        'status_display',
        'is_recent',
        'created_at',
        'updated_at'
    ]

    # Champs pour la recherche
    search_fields = [
        'name',
        'description',
        'nombre'
    ]

    # Filtres dans la barre latérale
    list_filter = [
        'is_active',
        'created_at',
        'updated_at'
    ]

    # Ordre par défaut
    ordering = ['-created_at']

    # Champs en lecture seule
    readonly_fields = [
        'created_at',
        'updated_at',
        'clickable_coordinates_form',
        'is_recent',
        'status_display'
    ]

    # Organisation des champs dans le formulaire
    fieldsets = (
        ("Informations générales", {
            'fields': (
                'name',
                'description',
                'nombre',
                'is_active'
            )
        }),
        ('Localisation GPS', {
            'fields': (
                'latitude',
                'longitude',
                'clickable_coordinates_form'
            )
        }),
        ('Informations calculées', {
            'fields': (
                'status_display',
                'is_recent',
            ),
            'classes': ('collapse',)
        }),
        ('Dates', {
            'fields': (
                'created_at',
                'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )

    # Pagination
    list_per_page = 25

    # Actions personnalisées
    actions = ['activate_offices', 'deactivate_offices']

    def activate_offices(self, request, queryset):
        """Action personnalisée pour activer les bureaux"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} bureau(x) de vote activé(s).')
    activate_offices.short_description = "Activer les bureaux sélectionnés"

    def deactivate_offices(self, request, queryset):
        """Action personnalisée pour désactiver les bureaux"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} bureau(x) de vote désactivé(s).')
    deactivate_offices.short_description = "Désactiver les bureaux sélectionnés"

    # Méthodes pour l'affichage dans la liste
    def clickable_coordinates(self, obj):
        """Afficher les coordonnées GPS comme lien cliquable vers Google Maps"""
        if obj.latitude and obj.longitude:
            google_maps_url = f"https://www.google.com/maps?q={obj.latitude},{obj.longitude}"
            return format_html(
                '<a href="{}" target="_blank" style="color: #0066cc; text-decoration: underline;">🗺️ {}, {}</a>',
                google_maps_url,
                obj.latitude,
                obj.longitude
            )
        return "Non défini"
    clickable_coordinates.short_description = "Coordonnées GPS"
    clickable_coordinates.allow_tags = True

    def clickable_coordinates_form(self, obj):
        """Afficher les coordonnées GPS comme lien cliquable pour le formulaire"""
        if obj.latitude and obj.longitude:
            google_maps_url = f"https://www.google.com/maps?q={obj.latitude},{obj.longitude}"
            return format_html(
                '<p><strong>Coordonnées:</strong> ({}, {})</p>'
                '<p><a href="{}" target="_blank" class="button" style="background: #417690; color: white; padding: 8px 16px; text-decoration: none; border-radius: 4px;">🗺️ Voir sur Google Maps</a></p>',
                obj.latitude,
                obj.longitude,
                google_maps_url
            )
        return "Coordonnées non définies"
    clickable_coordinates_form.short_description = "Voir sur la carte"
    clickable_coordinates_form.allow_tags = True

    def is_recent(self, obj):
        """Afficher si l'enregistrement est récent"""
        return obj.is_recent
    is_recent.short_description = "Récent (24h)"
    is_recent.boolean = True

    def status_display(self, obj):
        """Afficher le statut formaté"""
        return obj.status_display
    status_display.short_description = "Statut"
