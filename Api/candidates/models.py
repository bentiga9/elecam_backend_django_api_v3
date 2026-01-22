from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from elections.models import Election
from political_parties.models import PartiePolitique


class Candidat(models.Model):
    """
    Modèle représentant un candidat à une élection.
    Basé sur les données officielles du PDF des résultats.
    """
    election = models.ForeignKey(
        Election, 
        on_delete=models.CASCADE,
        related_name='candidats',
        verbose_name="Élection"
    )
    partie_politique = models.ForeignKey(
        PartiePolitique, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='candidats',
        verbose_name="Parti politique"
    )
    
    # Informations personnelles
    name = models.CharField(
        max_length=255,
        verbose_name="Nom complet"
    )
    
    # Métadonnées
    is_active = models.BooleanField(
        default=True,
        verbose_name="Est actif"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Créé le"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Mis à jour le"
    )

    def __str__(self):
        party_str = f" ({self.partie_politique.abbreviation})" if self.partie_politique else ""
        return f"{self.name}{party_str}"

    class Meta:
        db_table = 'candidat'
        verbose_name = "Candidat"
        verbose_name_plural = "Candidats"
        ordering = ['election', 'name']
        constraints = [
            models.UniqueConstraint(
                fields=['election', 'name'],
                name='unique_candidate_per_election'
            )
        ]


# Signals pour synchroniser automatiquement le compteur de candidats
@receiver(post_save, sender=Candidat)
def update_candidates_count_on_save(sender, instance, created, **kwargs):
    """Met à jour le compteur de candidats quand un candidat est créé ou modifié"""
    if instance.election_id:
        try:
            election = Election.objects.get(pk=instance.election_id)
            actual_count = election.candidats.count()
            if election.candidates_count != actual_count:
                # Éviter la récursion en utilisant update() au lieu de save()
                Election.objects.filter(pk=election.pk).update(candidates_count=actual_count)
        except Election.DoesNotExist:
            pass


@receiver(post_delete, sender=Candidat)
def update_candidates_count_on_delete(sender, instance, **kwargs):
    """Met à jour le compteur de candidats quand un candidat est supprimé"""
    if instance.election_id:
        try:
            election = Election.objects.get(pk=instance.election_id)
            actual_count = election.candidats.count()
            # Éviter la récursion en utilisant update() au lieu de save()
            Election.objects.filter(pk=election.pk).update(candidates_count=actual_count)
        except Election.DoesNotExist:
            pass