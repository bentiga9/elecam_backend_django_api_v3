from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from election_types.models import ElectionType


class CalendrierElectoral(models.Model):
    """
    Modèle pour gérer le calendrier électoral.
    Relation avec les types d'élection.
    Peut être lié à une élection spécifique pour le futur.
    """

    STATUS_CHOICES = [
        ('planifie', 'Planifié'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('reporte', 'Reporté'),
        ('annule', 'Annulé'),
    ]
    
    EVENT_TYPE_CHOICES = [
        ('election', 'Jour d\'élection'),
        ('inscription', 'Période d\'inscription'),
        ('campagne', 'Campagne électorale'),
        ('resultats', 'Proclamation des résultats'),
        ('contentieux', 'Délai de contentieux'),
        ('autre', 'Autre'),
    ]

    type_election = models.ForeignKey(
        ElectionType,
        on_delete=models.CASCADE,
        verbose_name="Type d'élection",
        help_text="Type d'élection associé"
    )
    
    # Lien optionnel vers une élection spécifique
    election = models.ForeignKey(
        'elections.Election',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='calendar_events',
        verbose_name="Élection",
        help_text="Élection spécifique associée"
    )
    
    title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Titre de l'événement",
        help_text="Titre descriptif de l'événement"
    )
    
    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPE_CHOICES,
        default='election',
        verbose_name="Type d'événement",
        help_text="Type d'événement du calendrier"
    )

    date = models.DateTimeField(
        verbose_name="Date et heure de l'événement",
        help_text="Date et heure prévues"
    )
    
    date_fin = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Date de fin",
        help_text="Date de fin (pour les périodes)"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='planifie',
        verbose_name="Statut",
        help_text="Statut actuel"
    )

    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Créé le",
        help_text="Date et heure de création de l'enregistrement"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Mis à jour le",
        help_text="Date et heure de dernière modification"
    )

    class Meta:
        db_table = 'calendrier_electoral_calendrierelectoral'
        verbose_name = "Calendrier électoral"
        verbose_name_plural = "Calendriers électoraux"
        ordering = ['-date']

    def __str__(self):
        return f"{self.type_election.name} - {self.date.strftime('%d/%m/%Y %H:%M')} ({self.get_status_display()})"

    def clean(self):
        """Validation personnalisée"""
        super().clean()

        # Vérifier que la date n'est pas dans le passé pour les nouvelles élections
        if not self.pk and self.date and self.date < timezone.now():
            raise ValidationError({
                'date': 'La date de l\'élection ne peut pas être dans le passé.'
            })

    def save(self, *args, **kwargs):
        """Sauvegarder avec validation complète"""
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def is_past(self):
        """Vérifier si l'élection est passée"""
        if not self.date:
            return False
        return self.date < timezone.now()

    @property
    def is_today(self):
        """Vérifier si l'élection est aujourd'hui"""
        if not self.date:
            return False
        return self.date.date() == timezone.now().date()

    @property
    def is_upcoming(self):
        """Vérifier si l'élection est à venir"""
        if not self.date:
            return False
        return self.date > timezone.now()

    @property
    def is_recent(self):
        """Vérifier si l'enregistrement est récent (moins de 24h)"""
        from datetime import timedelta
        return self.created_at >= timezone.now() - timedelta(hours=24)

    @property
    def days_until_election(self):
        """Calculer le nombre de jours jusqu'à l'élection"""
        if not self.date or self.is_past:
            return 0
        delta = self.date.date() - timezone.now().date()
        return delta.days

    @property
    def status_color(self):
        """Retourner une couleur pour le statut (pour l'affichage)"""
        colors = {
            'planifie': 'blue',
            'en_cours': 'green',
            'termine': 'gray',
            'reporte': 'orange',
            'annule': 'red',
        }
        return colors.get(self.status, 'black')
