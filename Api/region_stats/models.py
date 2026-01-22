from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from elections.models import Election
from regions.models import Region


class RegionStat(models.Model):
    """
    Statistiques électorales par région.
    Contient les données d'inscrits, votants, bulletins nuls, etc.
    au niveau régional (agrégées ou directes).
    """
    election = models.ForeignKey(
        Election,
        on_delete=models.CASCADE,
        related_name='region_stats',
        verbose_name="Élection"
    )
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name='election_stats',
        verbose_name="Région"
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
        db_table = 'department_stats_regionstat'  # Pointer vers la table existante
        verbose_name = "Statistique régionale"
        verbose_name_plural = "Statistiques régionales"
        ordering = ['election', 'region__region_type', 'region']
        constraints = [
            models.UniqueConstraint(
                fields=['election', 'region'],
                name='unique_stat_per_election_region'
            )
        ]

    def __str__(self):
        return f"{self.region.name} - {self.election.title}"

    def save(self, *args, **kwargs):
        # Calcul automatique du taux d'abstention si non fourni
        if self.inscrits > 0 and not self.taux_abstention:
            self.taux_abstention = 100 - self.taux_participation
        super().save(*args, **kwargs)
