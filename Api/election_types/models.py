from django.db import models
from django.utils import timezone


class ElectionType(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nom du type d'élection")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Mis à jour le")

    class Meta:
        verbose_name = "Type d'élection"
        verbose_name_plural = "Types d'élection"

    def __str__(self):
        return self.name