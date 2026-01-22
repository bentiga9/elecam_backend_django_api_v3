from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from elections.models import Election
from departments.models import Department


class DepartmentStat(models.Model):
    """
    Statistiques électorales par département.
    Contient les données d'inscrits, votants, bulletins nuls, etc.
    basées sur les résultats officiels du PDF.
    """
    election = models.ForeignKey(
        Election,
        on_delete=models.CASCADE,
        related_name='department_stats',
        verbose_name="Élection"
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='election_stats',
        verbose_name="Département"
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
        verbose_name = "Statistique départementale"
        verbose_name_plural = "Statistiques départementales"
        ordering = ['election', 'department__region', 'department']
        constraints = [
            models.UniqueConstraint(
                fields=['election', 'department'],
                name='unique_stat_per_election_department'
            )
        ]

    def __str__(self):
        return f"{self.department.name} - {self.election.title}"

    def save(self, *args, **kwargs):
        # Calcul automatique du taux d'abstention si non fourni
        if self.inscrits > 0 and not self.taux_abstention:
            self.taux_abstention = 100 - self.taux_participation
        super().save(*args, **kwargs)
