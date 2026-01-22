from django.contrib import admin
from .models import Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'region', 'chef_lieu', 'created_at')
    list_filter = ('region',)
    search_fields = ('name', 'code', 'chef_lieu')
    ordering = ('region', 'name')
    readonly_fields = ('created_at', 'updated_at')
