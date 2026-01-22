from django.db import models
from django.utils import timezone


class Region(models.Model):
    """
    Modèle représentant une région du Cameroun.
    Inclut les 10 régions nationales + la Diaspora (avec ses zones).
    """
    REGION_TYPE_CHOICES = [
        ('national', 'Région nationale'),
        ('diaspora', 'Zone diaspora'),
    ]
    
    name = models.CharField(
        max_length=100, 
        unique=True, 
        verbose_name="Nom de la région"
    )
    code = models.CharField(
        max_length=20, 
        unique=True, 
        verbose_name="Code unique"
    )
    region_type = models.CharField(
        max_length=20,
        choices=REGION_TYPE_CHOICES,
        default='national',
        verbose_name="Type de région"
    )
    chef_lieu = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Chef-lieu"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Est active"
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
        verbose_name = "Région"
        verbose_name_plural = "Régions"
        ordering = ['region_type', 'name']
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'code'],
                name='unique_region_name_code'
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.code})"
    
    @property
    def is_diaspora(self):
        return self.region_type == 'diaspora'
    
    @classmethod
    def get_national_regions(cls):
        """Retourne uniquement les régions nationales"""
        return cls.objects.filter(region_type='national', is_active=True)
    
    @classmethod
    def get_diaspora_zones(cls):
        """Retourne uniquement les zones diaspora"""
        return cls.objects.filter(region_type='diaspora', is_active=True)