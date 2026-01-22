from django.db import models

class PartiePolitique(models.Model):
    name = models.CharField(max_length=255, unique=True)
    abbreviation = models.CharField(max_length=10, unique=True, null=True, blank=True)
    logo_url = models.CharField(max_length=255, null=True, blank=True)
    color_hex = models.CharField(max_length=7, null=True, blank=True)  # Format: #228B22
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'partie_politique'