from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Avg, Count
from .models import RegionStat
from .serializers import (
    RegionStatSerializer,
    RegionStatListSerializer,
    RegionStatAggregateSerializer
)


class RegionStatViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour les statistiques par région.
    
    list: Liste toutes les statistiques régionales
    retrieve: Détails d'une statistique régionale
    by_type: Filtre les statistiques par type de région (national/diaspora)
    summary: Résumé global pour une élection
    """
    queryset = RegionStat.objects.select_related(
        'election', 
        'region'
    ).all()
    serializer_class = RegionStatSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['election', 'region', 'region__region_type']
    search_fields = ['region__name', 'election__title']
    ordering_fields = ['inscrits', 'votants', 'taux_participation', 'region__name']
    ordering = ['region__region_type', 'region__name']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'list':
            return RegionStatListSerializer
        return RegionStatSerializer

    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """
        Retourne les statistiques filtrées par type de région.
        Query params: 
        - election_id (required)
        - region_type (optional: 'national' ou 'diaspora')
        """
        election_id = request.query_params.get('election_id')
        region_type = request.query_params.get('region_type')
        
        if not election_id:
            return Response(
                {"error": "election_id est requis"}, 
                status=400
            )
        
        queryset = RegionStat.objects.filter(
            election_id=election_id
        ).select_related('region', 'election')
        
        if region_type:
            queryset = queryset.filter(region__region_type=region_type)
        
        serializer = RegionStatListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        Retourne un résumé global des statistiques régionales pour une élection.
        Query param: election_id (required)
        """
        election_id = request.query_params.get('election_id')
        
        if not election_id:
            return Response(
                {"error": "election_id est requis"}, 
                status=400
            )
        
        stats = RegionStat.objects.filter(
            election_id=election_id
        ).aggregate(
            total_inscrits=Sum('inscrits'),
            total_votants=Sum('votants'),
            taux_participation_global=Avg('taux_participation'),
            total_bulletins_nuls=Sum('bulletins_nuls'),
            total_suffrages_exprimes=Sum('suffrages_exprimes'),
            nombre_regions=Count('region')
        )
        
        # Statistiques par type de région
        national_stats = RegionStat.objects.filter(
            election_id=election_id,
            region__region_type='national'
        ).aggregate(
            inscrits_national=Sum('inscrits'),
            votants_national=Sum('votants'),
            nombre_regions_nationales=Count('region')
        )
        
        diaspora_stats = RegionStat.objects.filter(
            election_id=election_id,
            region__region_type='diaspora'
        ).aggregate(
            inscrits_diaspora=Sum('inscrits'),
            votants_diaspora=Sum('votants'),
            nombre_zones_diaspora=Count('region')
        )
        
        # Combiner tous les résultats
        stats.update(national_stats)
        stats.update(diaspora_stats)
        
        return Response(stats)
