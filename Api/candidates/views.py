from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from .models import Candidat
from .serializers import CandidatSerializer, CandidatListSerializer


@extend_schema_view(
    list=extend_schema(
        tags=['Candidats'],
        summary="Liste des candidats",
        description="Retourne la liste de tous les candidats avec leurs partis politiques.",
        parameters=[
            OpenApiParameter(name='election', description='Filtrer par élection (ID)', type=int),
            OpenApiParameter(name='partie_politique', description='Filtrer par parti politique (ID)', type=int),
            OpenApiParameter(name='search', description='Recherche par nom', type=str),
        ]
    ),
    create=extend_schema(
        tags=['Candidats'],
        summary="Créer un candidat",
        description="Crée un nouveau candidat pour une élection. Réservé aux administrateurs."
    )
)
class CandidatListCreateView(generics.ListCreateAPIView):
    """
    Liste et création de candidats
    OPTIMISATION: Requêtes avec select_related pour éviter N+1
    """
    queryset = Candidat.objects.select_related(
        'election__type', 'partie_politique'
    ).all()
    serializer_class = CandidatSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['election', 'partie_politique', 'is_active']
    search_fields = ['name']
    ordering_fields = ['name', 'ballot_number', 'created_at']
    ordering = ['ballot_number', 'name']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CandidatListSerializer
        return CandidatSerializer


@extend_schema_view(
    retrieve=extend_schema(
        tags=['Candidats'],
        summary="Détail d'un candidat",
        description="Retourne les détails complets d'un candidat."
    ),
    update=extend_schema(
        tags=['Candidats'],
        summary="Modifier un candidat",
        description="Modifie un candidat existant. Réservé aux administrateurs."
    ),
    partial_update=extend_schema(
        tags=['Candidats'],
        summary="Modifier partiellement un candidat",
        description="Modifie partiellement un candidat. Réservé aux administrateurs."
    ),
    destroy=extend_schema(
        tags=['Candidats'],
        summary="Supprimer un candidat",
        description="Supprime un candidat. Réservé aux administrateurs."
    )
)
class CandidatDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Détail, mise à jour et suppression d'un candidat
    OPTIMISATION: Requêtes optimisées
    """
    queryset = Candidat.objects.select_related(
        'election__type', 'partie_politique'
    ).all()
    serializer_class = CandidatSerializer