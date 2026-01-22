from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from elections.models import Election
from regions.models import Region


class DiasporaStat(models.Model):
    """
    Statistiques électorales pour les zones de la diaspora.
    Contient les données d'inscrits, votants, bulletins nuls, etc.
    pour chaque zone diaspora (Afrique, Amérique, Asie, Europe).
    """
    ZONE_CHOICES = [
        ('AFRIQUE', 'Afrique'),
        ('AMERIQUE', 'Amérique'),
        ('ASIE', 'Asie-Océanie'),
        ('EUROPE', 'Europe'),
    ]
    
    election = models.ForeignKey(
        Election,
        on_delete=models.CASCADE,
        related_name='diaspora_stats',
        verbose_name="Élection"
    )
    zone = models.CharField(
        max_length=20,
        choices=ZONE_CHOICES,
        verbose_name="Zone diaspora"
    )
    
    # Données de participation
    inscrits = models.PositiveIntegerField(
        default=0,
        verbose_name="Nombre d'inscrits",
        validators=[MinValueValidator(0)]
    )
    votants = models.PositiveIntegerField(
        default=0,
        verbose_name="Nombre de votants",
        validators=[MinValueValidator(0)]
    )
    taux_participation = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Taux de participation (%)"
    )
    taux_abstention = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Taux d'abstention (%)"
    )
    
    # Bulletins
    bulletins_nuls = models.PositiveIntegerField(
        default=0,
        verbose_name="Bulletins nuls",
        validators=[MinValueValidator(0)]
    )
    suffrages_exprimes = models.PositiveIntegerField(
        default=0,
        verbose_name="Suffrages valablement exprimés",
        validators=[MinValueValidator(0)]
    )
    
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Créé le"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Mis à jour le"
    )

    class Meta:
        verbose_name = "Statistique diaspora"
        verbose_name_plural = "Statistiques diaspora"
        ordering = ['election', 'zone']
        constraints = [
            models.UniqueConstraint(
                fields=['election', 'zone'],
                name='unique_stat_per_election_zone'
            )
        ]

    def __str__(self):
        return f"{self.get_zone_display()} - {self.election.title}"

    def save(self, *args, **kwargs):
        # Calcul automatique du taux d'abstention si non fourni
        if self.inscrits > 0 and not self.taux_abstention:
            self.taux_abstention = 100 - self.taux_participation
        super().save(*args, **kwargs)
