from django.contrib import admin
from .models import PartiePolitique

@admin.register(PartiePolitique)
class PartiePolitiqueAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviation', 'color_hex', 'created_at', 'updated_at')
    search_fields = ('name', 'abbreviation')
    list_filter = ('created_at', 'updated_at')
    ordering = ('name',)