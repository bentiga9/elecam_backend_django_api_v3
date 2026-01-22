from rest_framework import generics, filters, permissions
from rest_framework.decorators import api_view, permission_classes as perm_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from .models import Region
from .serializers import RegionSerializer, RegionListSerializer
from .permissions import AdminWriteOnlyPermission


@extend_schema_view(
    list=extend_schema(
        tags=['Régions'],
        summary="Liste des régions",
        description="Retourne la liste des 10 régions du Cameroun et des 4 zones diaspora.",
        parameters=[
            OpenApiParameter(name='region_type', description='Filtrer par type', type=str, enum=['national', 'diaspora']),
            OpenApiParameter(name='search', description='Recherche par nom ou code', type=str),
        ]
    ),
    create=extend_schema(
        tags=['Régions'],
        summary="Créer une région",
        description="Crée une nouvelle région. Réservé aux administrateurs."
    )
)
class RegionListCreateAPIView(generics.ListCreateAPIView):
    """
    Liste et création de régions.
    """
    queryset = Region.objects.prefetch_related('departments').all()
    serializer_class = RegionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['region_type', 'is_active']
    search_fields = ['name', 'code', 'chef_lieu']
    ordering_fields = ['name', 'code', 'region_type']
    ordering = ['region_type', 'name']
    permission_classes = [AdminWriteOnlyPermission]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RegionSerializer
        return RegionSerializer


@extend_schema_view(
    retrieve=extend_schema(
        tags=['Régions'],
        summary="Détail d'une région",
        description="Retourne les détails d'une région avec ses départements."
    ),
    update=extend_schema(
        tags=['Régions'],
        summary="Modifier une région",
        description="Modifie une région existante. Réservé aux administrateurs."
    ),
    partial_update=extend_schema(
        tags=['Régions'],
        summary="Modifier partiellement une région",
        description="Modifie partiellement une région. Réservé aux administrateurs."
    ),
    destroy=extend_schema(
        tags=['Régions'],
        summary="Supprimer une région",
        description="Supprime une région. Réservé aux administrateurs."
    )
)
class RegionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Détail, mise à jour et suppression d'une région.
    """
    queryset = Region.objects.prefetch_related('departments').all()
    serializer_class = RegionSerializer
    permission_classes = [AdminWriteOnlyPermission]