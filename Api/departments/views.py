from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from .models import Department
from .serializers import DepartmentSerializer, DepartmentListSerializer


@extend_schema_view(
    list=extend_schema(
        tags=['Départements'],
        summary="Liste des départements",
        description="Retourne la liste des 58 départements du Cameroun.",
        parameters=[
            OpenApiParameter(name='region', description='Filtrer par région (ID)', type=int),
            OpenApiParameter(name='search', description='Recherche par nom ou code', type=str),
        ]
    ),
    retrieve=extend_schema(
        tags=['Départements'],
        summary="Détail d'un département",
        description="Retourne les détails d'un département."
    ),
    create=extend_schema(
        tags=['Départements'],
        summary="Créer un département",
        description="Crée un nouveau département. Réservé aux administrateurs."
    ),
    update=extend_schema(
        tags=['Départements'],
        summary="Modifier un département",
        description="Modifie un département existant. Réservé aux administrateurs."
    ),
    partial_update=extend_schema(
        tags=['Départements'],
        summary="Modifier partiellement un département",
        description="Modifie partiellement un département. Réservé aux administrateurs."
    ),
    destroy=extend_schema(
        tags=['Départements'],
        summary="Supprimer un département",
        description="Supprime un département. Réservé aux administrateurs."
    )
)
class DepartmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des départements.
    
    list: Liste tous les départements
    retrieve: Détails d'un département
    create: Créer un département (admin)
    update: Modifier un département (admin)
    destroy: Supprimer un département (admin)
    """
    queryset = Department.objects.select_related('region').all()
    serializer_class = DepartmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['region', 'region__code']
    search_fields = ['name', 'code', 'chef_lieu']
    ordering_fields = ['name', 'region', 'created_at']
    ordering = ['region', 'name']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'list':
            return DepartmentListSerializer
        return DepartmentSerializer

    @extend_schema(
        tags=['Départements'],
        summary="Départements par région",
        description="Retourne les départements groupés par région."
    )
    @action(detail=False, methods=['get'])
    def by_region(self, request):
        """Retourne les départements groupés par région"""
        from regions.models import Region
        
        regions = Region.objects.prefetch_related('departments').all()
        result = {}
        
        for region in regions:
            result[region.name] = DepartmentListSerializer(
                region.departments.all(), 
                many=True
            ).data
        
        return Response(result)
