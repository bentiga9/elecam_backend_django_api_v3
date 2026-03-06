from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .models import CandidateRegionResult, CandidateDepartmentResult, CandidateGlobalResult, CandidateDiasporaResult
from .serializers import (
    CandidateGlobalResultSerializer,
    CandidateRegionResultSerializer,
    CandidateDepartmentResultSerializer,
    CandidateDiasporaResultSerializer
)


@extend_schema_view(
    list=extend_schema(
        tags=['Résultats des candidats'],
        summary="Classement général des candidats",
        description="Retourne le classement final des candidats pour une élection.",
        parameters=[
            OpenApiParameter(name='election', description='Filtrer par élection (ID)', type=int),
            OpenApiParameter(name='is_winner', description='Filtrer les gagnants uniquement', type=bool),
        ]
    ),
    retrieve=extend_schema(
        tags=['Résultats des candidats'],
        summary="Détail d'un résultat global",
        description="Retourne le détail du résultat global d'un candidat."
    ),
    create=extend_schema(
        tags=['Résultats des candidats'],
        summary="Créer un résultat global",
        description="Crée un résultat global pour un candidat. Réservé aux administrateurs."
    ),
    update=extend_schema(tags=['Résultats des candidats'], summary="Modifier un résultat global"),
    partial_update=extend_schema(tags=['Résultats des candidats'], summary="Modifier partiellement un résultat"),
    destroy=extend_schema(tags=['Résultats des candidats'], summary="Supprimer un résultat global")
)
class CandidateGlobalResultViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour les résultats globaux des candidats.
    Affiche le classement final d'une élection.
    """
    queryset = CandidateGlobalResult.objects.select_related(
        'election',
        'candidate',
        'candidate__partie_politique'
    ).all()
    serializer_class = CandidateGlobalResultSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['election', 'is_winner']
    ordering_fields = ['rang', 'pourcentage_national', 'total_suffrages']
    ordering = ['rang']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    @extend_schema(
        tags=['Résultats des candidats'],
        summary="Podium (Top 3)",
        description="Retourne les 3 premiers candidats d'une élection.",
        parameters=[OpenApiParameter(name='election_id', description='ID de l\'élection', type=int, required=True)]
    )
    @action(detail=False, methods=['get'])
    def podium(self, request):
        """Retourne le top 3 pour une élection"""
        election_id = request.query_params.get('election_id')
        
        if not election_id:
            return Response({"error": "election_id est requis"}, status=400)
        
        top3 = self.queryset.filter(
            election_id=election_id,
            rang__lte=3
        ).order_by('rang')
        
        serializer = self.get_serializer(top3, many=True)
        return Response(serializer.data)

    @extend_schema(
        tags=['Résultats des candidats'],
        summary="Gagnant de l'élection",
        description="Retourne le candidat élu d'une élection.",
        parameters=[OpenApiParameter(name='election_id', description='ID de l\'élection', type=int, required=True)]
    )
    @action(detail=False, methods=['get'])
    def winner(self, request):
        """Retourne le gagnant d'une élection"""
        election_id = request.query_params.get('election_id')
        
        if not election_id:
            return Response({"error": "election_id est requis"}, status=400)
        
        winner = self.queryset.filter(
            election_id=election_id,
            is_winner=True
        ).first()
        
        if not winner:
            return Response({"error": "Aucun gagnant trouvé"}, status=404)
        
        serializer = self.get_serializer(winner)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(
        tags=['Résultats des candidats'],
        summary="Résultats par région",
        description="Retourne les résultats des candidats par région.",
        parameters=[
            OpenApiParameter(name='election', description='Filtrer par élection (ID)', type=int),
            OpenApiParameter(name='candidate', description='Filtrer par candidat (ID)', type=int),
            OpenApiParameter(name='region', description='Filtrer par région (ID)', type=int),
        ]
    ),
    retrieve=extend_schema(tags=['Résultats des candidats'], summary="Détail d'un résultat régional"),
    create=extend_schema(tags=['Résultats des candidats'], summary="Créer un résultat régional"),
    update=extend_schema(tags=['Résultats des candidats'], summary="Modifier un résultat régional"),
    partial_update=extend_schema(tags=['Résultats des candidats'], summary="Modifier partiellement"),
    destroy=extend_schema(tags=['Résultats des candidats'], summary="Supprimer un résultat régional")
)
class CandidateRegionResultViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour les résultats régionaux des candidats.
    """
    queryset = CandidateRegionResult.objects.select_related(
        'election',
        'candidate',
        'candidate__partie_politique',
        'region'
    ).all()
    serializer_class = CandidateRegionResultSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['election', 'candidate', 'region']
    ordering_fields = ['pourcentage', 'suffrages', 'region__name']
    ordering = ['-pourcentage']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'])
    def by_candidate(self, request):
        """Résultats d'un candidat dans toutes les régions"""
        candidate_id = request.query_params.get('candidate_id')
        election_id = request.query_params.get('election_id')
        
        if not candidate_id or not election_id:
            return Response(
                {"error": "candidate_id et election_id sont requis"}, 
                status=400
            )
        
        results = self.queryset.filter(
            candidate_id=candidate_id,
            election_id=election_id
        ).order_by('-pourcentage')
        
        serializer = self.get_serializer(results, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_region(self, request):
        """Tous les candidats pour une région donnée"""
        region_id = request.query_params.get('region_id')
        election_id = request.query_params.get('election_id')
        
        if not region_id or not election_id:
            return Response(
                {"error": "region_id et election_id sont requis"}, 
                status=400
            )
        
        results = self.queryset.filter(
            region_id=region_id,
            election_id=election_id
        ).order_by('-pourcentage')
        
        serializer = self.get_serializer(results, many=True)
        return Response(serializer.data)


class CandidateDepartmentResultViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour les résultats départementaux des candidats.
    """
    queryset = CandidateDepartmentResult.objects.select_related(
        'election',
        'candidate',
        'candidate__partie_politique',
        'department',
        'department__region'
    ).all()
    serializer_class = CandidateDepartmentResultSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['election', 'candidate', 'department', 'department__region']
    ordering_fields = ['pourcentage', 'suffrages', 'department__name']
    ordering = ['-pourcentage']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'])
    def by_candidate(self, request):
        """Résultats d'un candidat dans tous les départements"""
        candidate_id = request.query_params.get('candidate_id')
        election_id = request.query_params.get('election_id')
        
        if not candidate_id or not election_id:
            return Response(
                {"error": "candidate_id et election_id sont requis"}, 
                status=400
            )
        
        results = self.queryset.filter(
            candidate_id=candidate_id,
            election_id=election_id
        ).order_by('department__region__name', '-pourcentage')
        
        serializer = self.get_serializer(results, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(
        tags=['Résultats des candidats'],
        summary="Résultats diaspora des candidats",
        description="Retourne les résultats agrégés des candidats pour la diaspora (4 zones).",
        parameters=[
            OpenApiParameter(name='election', description='Filtrer par élection (ID)', type=int),
            OpenApiParameter(name='candidate', description='Filtrer par candidat (ID)', type=int),
            OpenApiParameter(name='ordering', description='Trier par champ (ex: -pourcentage_diaspora)', type=str),
        ]
    ),
    retrieve=extend_schema(
        tags=['Résultats des candidats'],
        summary="Détail d'un résultat diaspora",
        description="Retourne le détail du résultat diaspora d'un candidat."
    ),
    create=extend_schema(
        tags=['Résultats des candidats'],
        summary="Créer un résultat diaspora",
        description="Crée un résultat diaspora pour un candidat. Réservé aux administrateurs."
    ),
    update=extend_schema(tags=['Résultats des candidats'], summary="Modifier un résultat diaspora"),
    partial_update=extend_schema(tags=['Résultats des candidats'], summary="Modifier partiellement un résultat diaspora"),
    destroy=extend_schema(tags=['Résultats des candidats'], summary="Supprimer un résultat diaspora")
)
class CandidateDiasporaResultViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour les résultats diaspora des candidats.
    Affiche les résultats agrégés des 4 zones diaspora.
    """
    queryset = CandidateDiasporaResult.objects.select_related(
        'election',
        'candidate',
        'candidate__partie_politique'
    ).all()
    serializer_class = CandidateDiasporaResultSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['election', 'candidate']
    ordering_fields = ['pourcentage_diaspora', 'total_suffrages_diaspora', 'created_at']
    ordering = ['-pourcentage_diaspora']
    search_fields = ['candidate__name', 'candidate__partie_politique__name']
    
    def get_permissions(self):
        """Permissions basées sur l'action"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]
    
    @extend_schema(
        tags=['Résultats des candidats'],
        summary="Classement diaspora",
        description="Retourne le classement des candidats pour la diaspora.",
        parameters=[
            OpenApiParameter(name='election', description='ID de l\'élection', required=True, type=int),
        ]
    )
    @action(detail=False, methods=['get'], url_path='ranking')
    def ranking(self, request):
        """
        Retourne le classement des candidats pour la diaspora.
        """
        election_id = request.query_params.get('election')
        if not election_id:
            return Response(
                {'error': 'Le paramètre election est requis'},
                status=400
            )
        
        results = self.queryset.filter(
            election_id=election_id
        ).order_by('-pourcentage_diaspora')
        
        serializer = self.get_serializer(results, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        tags=['Résultats des candidats'],
        summary="Résultats par zone diaspora",
        description="Retourne les résultats d'un candidat détaillés par zone diaspora.",
        parameters=[
            OpenApiParameter(name='candidate', description='ID du candidat', required=True, type=int),
            OpenApiParameter(name='election', description='ID de l\'élection', required=True, type=int),
        ]
    )
    @action(detail=False, methods=['get'], url_path='by-zone')
    def by_zone(self, request):
        """
        Retourne les détails par zone diaspora pour un candidat.
        """
        candidate_id = request.query_params.get('candidate')
        election_id = request.query_params.get('election')
        
        if not candidate_id or not election_id:
            return Response(
                {'error': 'Les paramètres candidate et election sont requis'},
                status=400
            )
        
        try:
            result = self.queryset.get(
                candidate_id=candidate_id,
                election_id=election_id
            )
        except CandidateDiasporaResult.DoesNotExist:
            return Response(
                {'error': 'Résultat non trouvé'},
                status=404
            )
        
        # Format détaillé avec les zones
        data = self.get_serializer(result).data
        data['zones'] = [
            {
                'name': 'Diaspora Afrique',
                'code': 'DA',
                'suffrages': result.suffrages_afrique
            },
            {
                'name': 'Diaspora Amérique',
                'code': 'DAM',
                'suffrages': result.suffrages_amerique
            },
            {
                'name': 'Diaspora Asie',
                'code': 'DAS',
                'suffrages': result.suffrages_asie
            },
            {
                'name': 'Diaspora Europe',
                'code': 'DE',
                'suffrages': result.suffrages_europe
            }
        ]
        
        return Response(data)
