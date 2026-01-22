from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


class PickupPoint(models.Model):
    """
    Modèle pour gérer les points de retrait des cartes électeurs.
    Les coordonnées GPS ne peuvent pas être négatives.
    Lié optionnellement à un département pour le futur.
    """

    name = models.CharField(
        max_length=255,
        verbose_name="Nom du point de retrait",
        help_text="Nom descriptif du point de retrait"
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description",
        help_text="Description détaillée du point de retrait"
    )

    nombre = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Numéro d'identification",
        help_text="Numéro ou code d'identification du point"
    )
    
    # Lien optionnel vers le département (pour le futur)
    department = models.ForeignKey(
        'departments.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pickup_points',
        verbose_name="Département",
        help_text="Département où se trouve le point de retrait"
    )
    
    address = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Adresse",
        help_text="Adresse complète du point de retrait"
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

    type = models.CharField(
        max_length=50,
        default="pickup_point",
        verbose_name="Type de point",
        help_text="Type du point de retrait"
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
        db_table = 'pickup_point_pickuppoint'
        verbose_name = "Point de retrait"
        verbose_name_plural = "Points de retrait"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.latitude}, {self.longitude})"

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
