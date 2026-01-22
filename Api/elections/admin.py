from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from .models import Election


class ElectionForm(forms.ModelForm):
    class Meta:
        model = Election
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Election présidentielle 2025'}),
            'description': forms.Textarea(attrs={'placeholder': 'Election du président de la république'}),
        }
    
    def clean_candidates_count(self):
        candidates_count = self.cleaned_data.get('candidates_count')
        if candidates_count is not None and candidates_count <= 0:
            raise ValidationError("Le nombre de candidats doit être supérieur à zéro.")
        return candidates_count
    
    def clean_progress_percentage(self):
        progress_percentage = self.cleaned_data.get('progress_percentage')
        if progress_percentage is not None:
            allowed_values = [25.00, 50.00, 75.00, 100.00]
            if progress_percentage not in allowed_values:
                raise ValidationError("Le pourcentage de progression doit être 25, 50, 75 ou 100.")
        return progress_percentage


@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    """
    Admin personnalisé pour le modèle Election.
    Affiche les champs importants.
    """
    form = ElectionForm

    # Champs affichés dans la liste - CORRECTION : utiliser les vrais noms de champs
    list_display = [
        'title',
        'type',
        'date',
        'status',
        'candidates_count',      # Utiliser le vrai nom du champ
        'progress_percentage',   # Utiliser le vrai nom du champ
        'created_at',
        'updated_at',
    ]

    # Champs filtrables
    list_filter = ['type', 'status', 'date', 'created_at', 'updated_at']

    # Champs recherchables
    search_fields = ['title', 'description']

    # Champs en lecture seule
    readonly_fields = ['created_at', 'updated_at']

    # Organisation des champs dans le formulaire
    fieldsets = (
        ('Informations générales', {
            'fields': ('title', 'type', 'date', 'description')
        }),
        ('État et progression', {
            'fields': ('status', 'candidates_count', 'progress_percentage', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )