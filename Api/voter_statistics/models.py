from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from elections.models import Election


class VoterStatistics(models.Model):
    """
    Statistiques globales d'une élection.
    Correspond au récapitulatif général du PDF (page 33).
    """
    election = models.OneToOneField(
        Election, 
        on_delete=models.CASCADE, 
        related_name='statistics',
        verbose_name="Élection",
        null=True,  # Temporaire pour migration - à retirer après
        blank=True
    )
    
    # Données de participation globales
    total_inscrits = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)], 
        verbose_name="Nombre total d'inscrits"
    )
    total_votants = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)], 
        verbose_name="Nombre total de votants"
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
    total_bulletins_nuls = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)], 
        verbose_name="Total bulletins nuls"
    )
    total_suffrages_exprimes = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)], 
        verbose_name="Total suffrages valablement exprimés"
    )
    
    # Distinction Cameroun / Diaspora (basé sur le PDF)
    inscrits_cameroun = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)], 
        verbose_name="Inscrits au Cameroun"
    )
    votants_cameroun = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)], 
        verbose_name="Votants au Cameroun"
    )
    inscrits_diaspora = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)], 
        verbose_name="Inscrits en Diaspora"
    )
    votants_diaspora = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)], 
        verbose_name="Votants en Diaspora"
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
        verbose_name = "Statistique électorale globale"
        verbose_name_plural = "Statistiques électorales globales"

    def __str__(self):
        return f"Statistiques pour {self.election.title}"
    
    def save(self, *args, **kwargs):
        # Calcul automatique du taux d'abstention
        if self.total_inscrits > 0 and not self.taux_abstention:
            self.taux_abstention = 100 - self.taux_participation
        super().save(*args, **kwargs)