from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


class VotingOffice(models.Model):
    """
    Modèle pour gérer les bureaux de vote.
    Les coordonnées GPS ne peuvent pas être négatives.
    Lié optionnellement à un département pour le futur.
    """

    name = models.CharField(
        max_length=255,
        verbose_name="Nom du bureau de vote",
        help_text="Nom descriptif du bureau de vote"
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description",
        help_text="Description détaillée du bureau de vote (horaires, etc.)"
    )

    nombre = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Numéro d'identification",
        help_text="Numéro ou code d'identification du bureau"
    )
    
    # Lien optionnel vers le département (pour le futur)
    department = models.ForeignKey(
        'departments.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='voting_offices',
        verbose_name="Département",
        help_text="Département où se trouve le bureau de vote"
    )
    
    address = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Adresse",
        help_text="Adresse complète du bureau de vote"
    )
    
    # Capacité du bureau
    capacity = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Capacité",
        help_text="Nombre maximum d'électeurs pouvant voter"
    )

    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        validators=[MinValueValidator(0.0)],
        verbose_name="Latitude",
        help_text="Coordonnée latitude (doit être positive)"
    )

    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        validators=[MinValueValidator(0.0)],
        verbose_name="Longitude",
        help_text="Coordonnée longitude (doit être positive)"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Bureau actif",
        help_text="Indique si le bureau de vote est actif"
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
        db_table = 'voting_office_votingoffice'
        verbose_name = "Bureau de vote"
        verbose_name_plural = "Bureaux de vote"
        ordering = ['-created_at']

    def __str__(self):
        status = "Actif" if self.is_active else "Inactif"
        return f"{self.name} ({status}) - ({self.latitude}, {self.longitude})"

    def clean(self):
        """Validation personnalisée pour s'assurer que les coordonnées sont positives"""
        super().clean()

        # Vérifier que latitude est positive
        if self.latitude < 0:
            raise ValidationError({
                'latitude': 'La latitude ne peut pas être négative.'
            })

        # Vérifier que longitude est positive
        if self.longitude < 0:
            raise ValidationError({
                'longitude': 'La longitude ne peut pas être négative.'
            })

        # Validation des limites géographiques (optionnel)
        if self.latitude > 90:
            raise ValidationError({
                'latitude': 'La latitude ne peut pas dépasser 90 degrés.'
            })

        if self.longitude > 180:
            raise ValidationError({
                'longitude': 'La longitude ne peut pas dépasser 180 degrés.'
            })

    def save(self, *args, **kwargs):
        """Sauvegarder avec validation complète"""
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def coordinates(self):
        """Retourner les coordonnées sous forme de tuple"""
        return (float(self.latitude), float(self.longitude))

    @property
    def is_recent(self):
        """Vérifier si l'enregistrement est récent (moins de 24h)"""
        from datetime import timedelta
        return self.created_at >= timezone.now() - timedelta(hours=24)

    @property
    def status_display(self):
        """Affichage du statut en français"""
        return "Actif" if self.is_active else "Inactif"
