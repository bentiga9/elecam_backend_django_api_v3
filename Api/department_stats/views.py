from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Avg, Count
from .models import DepartmentStat
from .serializers import (
    DepartmentStatSerializer, 
    DepartmentStatListSerializer
)


class DepartmentStatViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour les statistiques par département.
    
    list: Liste toutes les statistiques
    retrieve: Détails d'une statistique
    by_region: Statistiques agrégées par région
    by_election: Statistiques pour une élection spécifique
    """
    queryset = DepartmentStat.objects.select_related(
        'election', 
        'department', 
        'department__region'
    ).all()
    serializer_class = DepartmentStatSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['election', 'department', 'department__region']
    search_fields = ['department__name', 'election__title']
    ordering_fields = ['inscrits', 'votants', 'taux_participation', 'department__name']
    ordering = ['department__region', 'department__name']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'list':
            return DepartmentStatListSerializer
        return DepartmentStatSerializer

    @action(detail=False, methods=['get'])
    def by_region(self, request):
        """
        Retourne les statistiques agrégées par région pour une élection.
        Query param: election_id (required)
        """
        election_id = request.query_params.get('election_id')
        
        if not election_id:
            return Response(
                {"error": "election_id est requis"}, 
                status=400
            )
        
        stats = DepartmentStat.objects.filter(
            election_id=election_id
        ).values(
            'department__region__name',
            'department__region__code'
        ).annotate(
            total_inscrits=Sum('inscrits'),
            total_votants=Sum('votants'),
            taux_participation_moyen=Avg('taux_participation'),
            total_bulletins_nuls=Sum('bulletins_nuls'),
            total_suffrages_exprimes=Sum('suffrages_exprimes'),
            nombre_departements=Count('department')
        ).order_by('department__region__name')
        
        # Transformer les résultats
        result = []
        for stat in stats:
            result.append({
                'region_name': stat['department__region__name'],
                'region_code': stat['department__region__code'],
                'total_inscrits': stat['total_inscrits'],
                'total_votants': stat['total_votants'],
                'taux_participation_moyen': stat['taux_participation_moyen'],
                'total_bulletins_nuls': stat['total_bulletins_nuls'],
                'total_suffrages_exprimes': stat['total_suffrages_exprimes'],
                'nombre_departements': stat['nombre_departements']
            })
        
        # Pas de serializer pour l'agrégation, retour direct
        return Response(result)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        Retourne un résumé global pour une élection.
        Query param: election_id (required)
        """
        election_id = request.query_params.get('election_id')
        
        if not election_id:
            return Response(
                {"error": "election_id est requis"}, 
                status=400
            )
        
        stats = DepartmentStat.objects.filter(
            election_id=election_id
        ).aggregate(
            total_inscrits=Sum('inscrits'),
            total_votants=Sum('votants'),
            taux_participation_global=Avg('taux_participation'),
            total_bulletins_nuls=Sum('bulletins_nuls'),
            total_suffrages_exprimes=Sum('suffrages_exprimes'),
            nombre_departements=Count('department')
        )
        
        return Response(stats)
