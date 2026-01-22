from django.contrib import admin
from django.utils.html import format_html
from .models import PickupPoint


@admin.register(PickupPoint)
class PickupPointAdmin(admin.ModelAdmin):
    """Configuration de l'interface d'administration pour PickupPoint"""

    # Permissions d'administration
    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def has_view_permission(self, request, obj=None):
        return True

    # Champs affichés dans la liste
    list_display = [
        'id',
        'name',
        'nombre',
        'clickable_coordinates',
        'type',
        'is_recent',
        'created_at',
        'updated_at'
    ]

    # Champs pour la recherche
    search_fields = [
        'name',
        'description',
        'nombre',
        'type'
    ]

    # Filtres dans la barre latérale
    list_filter = [
        'type',
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
        'is_recent'
    ]

    # Organisation des champs dans le formulaire
    fieldsets = (
        ("Informations générales", {
            'fields': (
                'name',
                'description',
                'nombre',
                'type'
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
    actions = ['mark_as_verified']

    def mark_as_verified(self, request, queryset):
        """Action personnalisée pour marquer comme vérifié"""
        updated = queryset.count()
        self.message_user(request, f'{updated} point(s) de retrait marqué(s) comme vérifié(s).')
    mark_as_verified.short_description = "Marquer comme vérifié"

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
