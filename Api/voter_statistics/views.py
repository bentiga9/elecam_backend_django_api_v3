from rest_framework import generics, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from .models import VoterStatistics
from .serializers import VoterStatisticsSerializer, VoterStatisticsSummarySerializer
from .permissions import AdminWriteOnlyPermission
from utils.cache_service import CacheService, cache_view_response


@extend_schema_view(
    list=extend_schema(
        tags=['Statistiques globales'],
        summary="Liste des statistiques électorales",
        description="Retourne les statistiques globales de participation pour chaque élection.",
        parameters=[
            OpenApiParameter(name='election', description='Filtrer par élection (ID)', type=int),
            OpenApiParameter(name='search', description='Recherche par titre d\'élection', type=str),
        ]
    ),
    create=extend_schema(
        tags=['Statistiques globales'],
        summary="Créer des statistiques",
        description="Crée des statistiques globales pour une élection. Réservé aux administrateurs."
    )
)
class VoterStatisticsListCreateAPIView(generics.ListCreateAPIView):
    """
    Liste et création de statistiques électorales avec cache Redis.
    Statistiques: inscrits, votants, taux de participation, bulletins nuls, suffrages exprimés.
    """
    queryset = VoterStatistics.objects.select_related('election', 'election__type').all()
    serializer_class = VoterStatisticsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['election', 'election__type']
    search_fields = ['election__title']
    ordering_fields = ['created_at', 'taux_participation', 'total_inscrits']
    ordering = ['-created_at']
    permission_classes = [AdminWriteOnlyPermission]

    @cache_view_response(timeout=600, vary_on_user=False)  # Cache 10 minutes
    def list(self, request, *args, **kwargs):
        """Liste avec cache Redis des réponses"""
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'GET' and self.request.query_params.get('summary'):
            return VoterStatisticsSummarySerializer
        return VoterStatisticsSerializer


@extend_schema_view(
    retrieve=extend_schema(
        tags=['Statistiques globales'],
        summary="Détail des statistiques",
        description="Retourne les statistiques détaillées d'une élection."
    ),
    update=extend_schema(
        tags=['Statistiques globales'],
        summary="Modifier les statistiques",
        description="Modifie les statistiques d'une élection. Réservé aux administrateurs."
    ),
    partial_update=extend_schema(
        tags=['Statistiques globales'],
        summary="Modifier partiellement les statistiques",
        description="Modifie partiellement les statistiques. Réservé aux administrateurs."
    ),
    destroy=extend_schema(
        tags=['Statistiques globales'],
        summary="Supprimer les statistiques",
        description="Supprime les statistiques d'une élection. Réservé aux administrateurs."
    )
)
class VoterStatisticsDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Détail, mise à jour et suppression de statistiques électorales.
    """
    queryset = VoterStatistics.objects.select_related('election', 'election__type').all()
    serializer_class = VoterStatisticsSerializer
    permission_classes = [AdminWriteOnlyPermission]