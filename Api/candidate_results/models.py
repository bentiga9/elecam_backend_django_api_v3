from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from elections.models import Election
from candidates.models import Candidat
from departments.models import Department
from regions.models import Region


class CandidateRegionResult(models.Model):
    """
    Résultats d'un candidat par région.
    Correspond aux totaux régionaux du PDF officiel.
    """
    election = models.ForeignKey(
        Election,
        on_delete=models.CASCADE,
        related_name='candidate_region_results',
        verbose_name="Élection"
    )
    candidate = models.ForeignKey(
        Candidat,
        on_delete=models.CASCADE,
        related_name='region_results',
        verbose_name="Candidat"
    )
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name='candidate_results',
        verbose_name="Région"
    )
    
    # Résultats
    suffrages = models.PositiveIntegerField(
        default=0,
        verbose_name="Suffrages obtenus (SVE)",
        validators=[MinValueValidator(0)]
    )
    pourcentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Pourcentage (%)"
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
        verbose_name = "Résultat régional du candidat"
        verbose_name_plural = "Résultats régionaux des candidats"
        ordering = ['election', 'region', '-pourcentage']
        constraints = [
            models.UniqueConstraint(
                fields=['election', 'candidate', 'region'],
                name='unique_candidate_region_result'
            )
        ]

    def __str__(self):
        return f"{self.candidate.name} - {self.region.name}: {self.pourcentage}%"


class CandidateDepartmentResult(models.Model):
    """
    Résultats d'un candidat par département.
    Correspond aux détails départementaux du PDF officiel.
    """
    election = models.ForeignKey(
        Election,
        on_delete=models.CASCADE,
        related_name='candidate_department_results',
        verbose_name="Élection"
    )
    candidate = models.ForeignKey(
        Candidat,
        on_delete=models.CASCADE,
        related_name='department_results',
        verbose_name="Candidat"
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='candidate_results',
        verbose_name="Département"
    )
    
    # Résultats
    suffrages = models.PositiveIntegerField(
        default=0,
        verbose_name="Suffrages obtenus (SVE)",
        validators=[MinValueValidator(0)]
    )
    pourcentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Pourcentage (%)"
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
        verbose_name = "Résultat départemental du candidat"
        verbose_name_plural = "Résultats départementaux des candidats"
        ordering = ['election', 'department__region', 'department', '-pourcentage']
        constraints = [
            models.UniqueConstraint(
                fields=['election', 'candidate', 'department'],
                name='unique_candidate_department_result'
            )
        ]

    def __str__(self):
        return f"{self.candidate.name} - {self.department.name}: {self.pourcentage}%"


class CandidateDiasporaResult(models.Model):
    """
    Résultats agrégés d'un candidat pour la diaspora.
    Agrège les résultats des 4 zones diaspora (Afrique, Amérique, Asie, Europe).
    """
    election = models.ForeignKey(
        Election,
        on_delete=models.CASCADE,
        related_name='candidate_diaspora_results',
        verbose_name="Élection"
    )
    candidate = models.ForeignKey(
        Candidat,
        on_delete=models.CASCADE,
        related_name='diaspora_results',
        verbose_name="Candidat"
    )
    
    # Résultats agrégés diaspora
    total_suffrages_diaspora = models.PositiveIntegerField(
        default=0,
        verbose_name="Total suffrages diaspora",
        validators=[MinValueValidator(0)],
        help_text="Somme des suffrages des 4 zones diaspora"
    )
    pourcentage_diaspora = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Pourcentage diaspora (%)",
        help_text="Pourcentage par rapport aux suffrages exprimés de la diaspora"
    )
    
    # Détails par zone
    suffrages_afrique = models.PositiveIntegerField(
        default=0,
        verbose_name="Suffrages Diaspora Afrique",
        validators=[MinValueValidator(0)]
    )
    suffrages_amerique = models.PositiveIntegerField(
        default=0,
        verbose_name="Suffrages Diaspora Amérique",
        validators=[MinValueValidator(0)]
    )
    suffrages_asie = models.PositiveIntegerField(
        default=0,
        verbose_name="Suffrages Diaspora Asie",
        validators=[MinValueValidator(0)]
    )
    suffrages_europe = models.PositiveIntegerField(
        default=0,
        verbose_name="Suffrages Diaspora Europe",
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
        verbose_name = "Résultat diaspora du candidat"
        verbose_name_plural = "Résultats diaspora des candidats"
        ordering = ['election', '-pourcentage_diaspora']
        constraints = [
            models.UniqueConstraint(
                fields=['election', 'candidate'],
                name='unique_candidate_diaspora_result'
            )
        ]

    def __str__(self):
        return f"{self.candidate.name} - Diaspora: {self.pourcentage_diaspora}%"


class CandidateGlobalResult(models.Model):
    """
    Résultat global d'un candidat pour une élection.
    Correspond au classement final du PDF (page 36).
    """
    election = models.ForeignKey(
        Election,
        on_delete=models.CASCADE,
        related_name='global_results',
        verbose_name="Élection"
    )
    candidate = models.ForeignKey(
        Candidat,
        on_delete=models.CASCADE,
        related_name='global_results',
        verbose_name="Candidat"
    )
    
    # Classement
    rang = models.PositiveIntegerField(
        default=1,
        verbose_name="Rang/Position",
        validators=[MinValueValidator(1)]
    )
    
    # Résultats globaux
    total_suffrages = models.PositiveIntegerField(
        default=0,
        verbose_name="Total suffrages obtenus",
        validators=[MinValueValidator(0)]
    )
    pourcentage_national = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Pourcentage national (%)"
    )
    
    # Indicateur de victoire
    is_winner = models.BooleanField(
        default=False,
        verbose_name="Est élu/gagnant"
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
        verbose_name = "Résultat global du candidat"
        verbose_name_plural = "Résultats globaux des candidats"
        ordering = ['election', 'rang']
        constraints = [
            models.UniqueConstraint(
                fields=['election', 'candidate'],
                name='unique_candidate_global_result'
            ),
            models.UniqueConstraint(
                fields=['election', 'rang'],
                name='unique_rank_per_election'
            )
        ]

    def __str__(self):
        winner_str = " (ÉLU)" if self.is_winner else ""
        return f"{self.rang}. {self.candidate.name} - {self.pourcentage_national}%{winner_str}"
