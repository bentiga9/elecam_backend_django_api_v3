from django.contrib import admin
from .models import CalendrierElectoral


@admin.register(CalendrierElectoral)
class CalendrierElectoralAdmin(admin.ModelAdmin):
    """Configuration de l'interface d'administration pour CalendrierElectoral"""

    # Champs affichés dans la liste
    list_display = [
        'id',
        'type_election',
        'date',
        'status',
        'status_display_colored',
        'days_until_election',
        'is_today',
        'is_recent',
        'created_at',
        'updated_at'
    ]

    # Champs pour la recherche
    search_fields = [
        'type_election__name',
        'status'
    ]

    # Filtres dans la barre latérale
    list_filter = [
        'status',
        'type_election',
        'date',
        'created_at',
        'updated_at'
    ]

    # Ordre par défaut
    ordering = ['-date']

    # Champs en lecture seule
    readonly_fields = [
        'created_at',
        'updated_at',
        'is_past',
        'is_today',
        'is_upcoming',
        'is_recent',
        'days_until_election',
        'status_color'
    ]

    # Organisation des champs dans le formulaire
    fieldsets = (
        ("Informations de l'élection", {
            'fields': (
                'type_election',
                'date',
                'status'
            )
        }),
        ('Informations calculées', {
            'fields': (
                'is_past',
                'is_today',
                'is_upcoming',
                'days_until_election',
                'status_color',
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
    actions = ['mark_as_en_cours', 'mark_as_termine', 'mark_as_reporte']

    def mark_as_en_cours(self, request, queryset):
        """Action personnalisée pour marquer comme en cours"""
        updated = queryset.update(status='en_cours')
        self.message_user(request, f'{updated} élection(s) marquée(s) comme en cours.')
    mark_as_en_cours.short_description = "Marquer comme 'En cours'"

    def mark_as_termine(self, request, queryset):
        """Action personnalisée pour marquer comme terminé"""
        updated = queryset.update(status='termine')
        self.message_user(request, f'{updated} élection(s) marquée(s) comme terminée(s).')
    mark_as_termine.short_description = "Marquer comme 'Terminé'"

    def mark_as_reporte(self, request, queryset):
        """Action personnalisée pour marquer comme reporté"""
        updated = queryset.update(status='reporte')
        self.message_user(request, f'{updated} élection(s) marquée(s) comme reportée(s).')
    mark_as_reporte.short_description = "Marquer comme 'Reporté'"

    # Méthodes pour l'affichage dans la liste
    def status_display_colored(self, obj):
        """Afficher le statut avec couleur"""
        color = obj.status_color
        return f'<span style="color: {color}; font-weight: bold;">{obj.get_status_display()}</span>'
    status_display_colored.short_description = "Statut"
    status_display_colored.allow_tags = True

    def days_until_election(self, obj):
        """Afficher le nombre de jours jusqu'à l'élection"""
        days = obj.days_until_election
        if obj.is_past:
            return f"Passée"
        elif obj.is_today:
            return f"Aujourd'hui"
        elif days == 1:
            return f"Demain"
        else:
            return f"Dans {days} jours"
    days_until_election.short_description = "Échéance"

    def is_today(self, obj):
        """Afficher si l'élection est aujourd'hui"""
        return obj.is_today
    is_today.short_description = "Aujourd'hui"
    is_today.boolean = True

    def is_recent(self, obj):
        """Afficher si l'enregistrement est récent"""
        return obj.is_recent
    is_recent.short_description = "Récent (24h)"
    is_recent.boolean = True
