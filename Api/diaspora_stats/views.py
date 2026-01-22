from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Avg, Count
from django_filters.rest_framework import DjangoFilterBackend
from .models import DiasporaStat
from .serializers import DiasporaStatSerializer, DiasporaStatListSerializer


class DiasporaStatViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour les statistiques de la diaspora.
    
    Endpoints disponibles:
    - list: Liste toutes les statistiques diaspora
    - retrieve: Détails d'une statistique
    - create: Créer une nouvelle statistique (admin)
    - update: Mettre à jour une statistique (admin)
    - delete: Supprimer une statistique (admin)
    - by_election: Statistiques par élection
    - by_zone: Statistiques par zone
    - aggregate: Statistiques agrégées de toute la diaspora
    """
    queryset = DiasporaStat.objects.all()
    serializer_class = DiasporaStatSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['election', 'zone']
    search_fields = ['zone', 'election__title']
    ordering_fields = ['zone', 'inscrits', 'votants', 'taux_participation']
    ordering = ['election', 'zone']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return DiasporaStatListSerializer
        return DiasporaStatSerializer
    
    @action(detail=False, methods=['get'], url_path='by-election/(?P<election_id>[^/.]+)')
    def by_election(self, request, election_id=None):
        """
        Retourne toutes les statistiques diaspora pour une élection donnée.
        
        Paramètres:
        - election_id: ID de l'élection
        """
        stats = self.queryset.filter(election_id=election_id)
        serializer = self.get_serializer(stats, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='by-zone/(?P<zone>[^/.]+)')
    def by_zone(self, request, zone=None):
        """
        Retourne toutes les statistiques pour une zone diaspora donnée.
        
        Paramètres:
        - zone: Code de la zone (AFRIQUE, AMERIQUE, ASIE, EUROPE)
        """
        stats = self.queryset.filter(zone=zone)
        serializer = self.get_serializer(stats, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='aggregate/(?P<election_id>[^/.]+)')
    def aggregate(self, request, election_id=None):
        """
        Retourne les statistiques agrégées de toute la diaspora pour une élection.
        
        Paramètres:
        - election_id: ID de l'élection
        
        Retourne:
        - total_inscrits: Total des inscrits diaspora
        - total_votants: Total des votants diaspora
        - taux_participation_moyen: Taux de participation moyen
        - total_bulletins_nuls: Total des bulletins nuls
        - total_suffrages_exprimes: Total des suffrages exprimés
        - nombre_zones: Nombre de zones diaspora
        - details_par_zone: Détails pour chaque zone
        """
        stats = self.queryset.filter(election_id=election_id).aggregate(
            total_inscrits=Sum('inscrits'),
            total_votants=Sum('votants'),
            taux_participation_moyen=Avg('taux_participation'),
            total_bulletins_nuls=Sum('bulletins_nuls'),
            total_suffrages_exprimes=Sum('suffrages_exprimes'),
            nombre_zones=Count('zone')
        )
        
        # Ajouter les détails par zone
        details_par_zone = self.queryset.filter(election_id=election_id)
        stats['details_par_zone'] = DiasporaStatListSerializer(details_par_zone, many=True).data
        
        return Response(stats)
