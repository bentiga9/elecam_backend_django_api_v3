import random
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from election_types.models import ElectionType


class ElectionManager(models.Manager):
    """Manager optimisé pour les élections"""

    def with_relations(self):
        """Retourne les élections avec leurs relations optimisées"""
        return self.select_related('type').prefetch_related(
            'candidat_set__partie_politique'
        )

    def active(self):
        """Retourne les élections actives (pending ou ongoing)"""
        return self.filter(status__in=['pending', 'ongoing'], is_active=True)

    def completed(self):
        """Retourne les élections terminées"""
        return self.filter(status='completed')

    def by_year(self, year):
        """Retourne les élections d'une année donnée"""
        return self.filter(date__year=year)


class Election(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('ongoing', 'En cours'),
        ('completed', 'Terminée'),
    ]

    PROGRESS_CHOICES = [
        (25.00, '25%'),
        (50.00, '50%'),
        (75.00, '75%'),
        (100.00, '100%'),
    ]

    title = models.CharField(max_length=150, verbose_name="Titre de l'élection")
    type = models.ForeignKey(ElectionType, on_delete=models.CASCADE, verbose_name="Type d'élection")
    date = models.DateField(verbose_name="Date de l'élection")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="État de l'élection")
    candidates_count = models.IntegerField(default=0, validators=[MinValueValidator(0)], verbose_name="Nombre de candidats")
    progress_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0.00,
        choices=PROGRESS_CHOICES,
        null=True,
        blank=True,
        verbose_name="Pourcentage de progression"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Détails optionnels")
    is_active = models.BooleanField(default=True, verbose_name="Est actif")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Mis à jour le")

    # Manager optimisé
    objects = ElectionManager()

    class Meta:
        verbose_name = "Élection"
        verbose_name_plural = "Élections"
        constraints = [
            models.UniqueConstraint(fields=['type', 'date'], name='unique_election_type_date')
        ]

    def clean(self):
        super().clean()
        if self.candidates_count < 0:
            raise ValidationError({
                'candidates_count': 'Le nombre de candidats ne peut pas être négatif.'
            })
                
        if self.progress_percentage is not None:
            allowed_values = [25.00, 50.00, 75.00, 100.00]
            if self.progress_percentage not in allowed_values:
                raise ValidationError({
                    'progress_percentage': 'Le pourcentage de progression doit être 25, 50, 75 ou 100.'
                })
        
        # Vérifier les doublons de type par année
        if self.type and self.date:
            # Vérifier s'il existe déjà une élection du même type la même année
            existing_elections = Election.objects.filter(
                type=self.type,
                date__year=self.date.year
            )
            if self.pk:
                existing_elections = existing_elections.exclude(pk=self.pk)
            
            if existing_elections.exists():
                raise ValidationError({
                    'type': f"Il existe déjà une élection de type '{self.type}' pour l'année {self.date.year}."
                })

    def save(self, *args, **kwargs):
        # If progress_percentage is not set or is 0, randomly set it to one of the allowed values
        if not self.progress_percentage or self.progress_percentage == 0.00:
            # Randomly choose from the allowed progress values
            allowed_values = [25.00, 50.00, 75.00, 100.00]
            self.progress_percentage = random.choice(allowed_values)

        # Appeler la validation complète avant la sauvegarde
        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.type.name} - {self.date.year})"