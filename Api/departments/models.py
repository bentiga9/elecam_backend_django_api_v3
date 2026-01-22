from django.db import models
from django.utils import timezone
from regions.models import Region


class Department(models.Model):
    """
    Modèle représentant un département du Cameroun.
    Le Cameroun compte 58 départements répartis dans 10 régions + zones diaspora.
    """
    name = models.CharField(
        max_length=100, 
        verbose_name="Nom du département"
    )
    code = models.CharField(
        max_length=20, 
        unique=True, 
        verbose_name="Code unique"
    )
    region = models.ForeignKey(
        Region, 
        on_delete=models.CASCADE, 
        related_name='departments',
        verbose_name="Région"
    )
    chef_lieu = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name="Chef-lieu"
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
        verbose_name = "Département"
        verbose_name_plural = "Départements"
        ordering = ['region', 'name']
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'region'],
                name='unique_department_name_per_region'
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.region.name})"
