from rest_framework import generics, filters, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Count
from rest_framework.exceptions import ValidationError as DRFValidationError
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from .models import Election
from election_types.models import ElectionType
from .serializers import ElectionSerializer, ElectionTypeSerializer
from .permissions import AdminWriteOnlyPermission
from utils.cache_service import cache_view_response, CacheService


@extend_schema_view(
    list=extend_schema(
        tags=['Élections'],
        summary="Liste des élections",
        description="Retourne la liste de toutes les élections avec filtres, recherche et tri.",
        parameters=[
            OpenApiParameter(name='type', description='Filtrer par type d\'élection (ID)', type=int),
            OpenApiParameter(name='status', description='Filtrer par statut', type=str, enum=['pending', 'ongoing', 'completed']),
            OpenApiParameter(name='date_filter', description='Filtrer par date', type=str, enum=['future', 'past', 'today']),
            OpenApiParameter(name='active_only', description='Afficher uniquement les élections actives', type=bool),
            OpenApiParameter(name='search', description='Recherche par titre ou description', type=str),
            OpenApiParameter(name='ordering', description='Tri (date, created_at, title)', type=str),
        ]
    ),
    create=extend_schema(
        tags=['Élections'],
        summary="Créer une élection",
        description="Crée une nouvelle élection. Réservé aux administrateurs."
    )
)
class ElectionListCreateAPIView(generics.ListCreateAPIView):
    """
    Liste et création d'élections avec filtres, recherche et tri.
    OPTIMISATION: Requêtes avec select_related pour éviter N+1 + Cache Redis
    """
    queryset = Election.objects.select_related('type').all()
    serializer_class = ElectionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'status']
    search_fields = ['title', 'description']
    ordering_fields = ['date', 'created_at', 'title']
    ordering = ['-date']
    permission_classes = [AdminWriteOnlyPermission]

    # @cache_view_response(timeout=600, vary_on_user=False)  # Cache désactivé temporairement
    def list(self, request, *args, **kwargs):
        """Liste des élections (cache désactivé temporairement)"""
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        """
        Filtrage personnalisé :
        - date_filter: 'future', 'past', 'today'
        - active_only: 'true'
        """
        print(f"🗄️  LECTURE BD: Requête PostgreSQL pour les élections")
        queryset = super().get_queryset()
        date_filter = self.request.query_params.get('date_filter')
        active_only = self.request.query_params.get('active_only')

        today = timezone.now().date()

        if date_filter == 'future':
            queryset = queryset.filter(date__gt=today)
        elif date_filter == 'past':
            queryset = queryset.filter(date__lt=today)
        elif date_filter == 'today':
            queryset = queryset.filter(date=today)

        if active_only and active_only.lower() == 'true':
            queryset = queryset.filter(status__in=['pending', 'ongoing'])

        return queryset

    def perform_create(self, serializer):
        """
        Validation supplémentaire lors de la création d'une élection
        """
        serializer.save()


@extend_schema_view(
    retrieve=extend_schema(
        tags=['Élections'],
        summary="Détail d'une élection",
        description="Retourne les détails complets d'une élection avec ses candidats."
    ),
    update=extend_schema(
        tags=['Élections'],
        summary="Modifier une élection",
        description="Modifie une élection existante. Réservé aux administrateurs."
    ),
    partial_update=extend_schema(
        tags=['Élections'],
        summary="Modifier partiellement une élection",
        description="Modifie partiellement une élection. Réservé aux administrateurs."
    ),
    destroy=extend_schema(
        tags=['Élections'],
        summary="Supprimer une élection",
        description="Supprime une élection. Impossible si l'élection est en cours."
    )
)
class ElectionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Détail, mise à jour et suppression d'une élection.
    OPTIMISATION: Requêtes optimisées avec prefetch_related pour les candidats
    """
    queryset = Election.objects.select_related('type').prefetch_related(
        'candidat_set__partie_politique'
    ).all()
    serializer_class = ElectionSerializer
    permission_classes = [AdminWriteOnlyPermission]

    def perform_update(self, serializer):
        """
        Validation supplémentaire lors de la mise à jour d'une élection
        """
        instance = serializer.save()
        # Actions supplémentaires possibles (logs, notifications)
        return instance

    def perform_destroy(self, instance):
        if instance.status == 'ongoing':
            raise DRFValidationError("Impossible de supprimer une élection en cours.")
        super().perform_destroy(instance)


@extend_schema(
    tags=['Élections'],
    summary="Statistiques des élections",
    description="Retourne les statistiques globales sur les élections (total, par statut, par type).",
    responses={200: OpenApiTypes.OBJECT}
)
@api_view(['GET'])
@permission_classes([permissions.AllowAny])  # Autoriser l'accès sans authentification
@cache_view_response(timeout=600, vary_on_user=False)  # Cache pour 10 minutes
def election_statistics(request):
    """
    Statistiques sur les élections.
    """
    elections = Election.objects.all()

    elections_by_status = dict(
        elections.values('status')
        .annotate(count=Count('id'))
        .values_list('status', 'count')
    )

    elections_by_type = dict(
        elections.values('type__name')
        .annotate(count=Count('id'))
        .values_list('type__name', 'count')
    )

    stats = {
        'total_elections': elections.count(),
        'elections_by_status': elections_by_status,
        'elections_by_type': elections_by_type,
        'upcoming_elections': elections.filter(
            date__gt=timezone.now().date(),
            status='pending'
        ).count(),
    }

    return Response(stats)