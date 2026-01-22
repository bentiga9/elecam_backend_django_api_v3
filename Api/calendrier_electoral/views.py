from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
import json
from datetime import datetime, timedelta
from .models import CalendrierElectoral
from .serializers import CalendrierElectoralSerializer, CalendrierElectoralUpcomingSerializer


class CalendrierElectoralViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer le calendrier électoral via API REST
    GET: Accès libre, POST/PUT/DELETE: Authentification requise
    """
    queryset = CalendrierElectoral.objects.all()
    serializer_class = CalendrierElectoralSerializer

    def get_permissions(self):
        """
        Permissions en fonction de la méthode HTTP
        GET: Libre accès
        POST/PUT/DELETE: Authentification requise
        """
        if self.action in ['list', 'retrieve', 'statistics', 'upcoming', 'today', 'by_status', 'recent', 'by_type']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """Filtrage et recherche personnalisée"""
        print(f"🗄️  LECTURE BD: Requête PostgreSQL pour calendrier_electoral")
        queryset = CalendrierElectoral.objects.select_related('type_election').all()

        # Filtrage par statut
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # Filtrage par type d'élection
        type_election = self.request.query_params.get('type_election')
        if type_election:
            queryset = queryset.filter(type_election_id=type_election)

        # Filtrage par plage de dates
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)

        # Recherche textuelle
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(type_election__name__icontains=search) |
                Q(status__icontains=search)
            )

        return queryset.order_by('-date')

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Action personnalisée pour obtenir des statistiques"""
        queryset = self.get_queryset()
        total = queryset.count()

        if total == 0:
            return Response({
                'total_elections': 0,
                'elections_planifiees': 0,
                'elections_en_cours': 0,
                'elections_terminees': 0,
                'elections_reportees': 0,
                'elections_annulees': 0,
                'elections_today': 0,
                'elections_upcoming': 0,
                'elections_past': 0
            })

        # Statistiques par statut
        status_counts = queryset.values('status').annotate(count=Count('status'))
        status_dict = {item['status']: item['count'] for item in status_counts}

        # Statistiques temporelles
        today = timezone.now().date()
        elections_today = len([obj for obj in queryset if obj.is_today])
        elections_upcoming = len([obj for obj in queryset if obj.is_upcoming])
        elections_past = len([obj for obj in queryset if obj.is_past])

        stats = {
            'total_elections': total,
            'elections_planifiees': status_dict.get('planifie', 0),
            'elections_en_cours': status_dict.get('en_cours', 0),
            'elections_terminees': status_dict.get('termine', 0),
            'elections_reportees': status_dict.get('reporte', 0),
            'elections_annulees': status_dict.get('annule', 0),
            'elections_today': elections_today,
            'elections_upcoming': elections_upcoming,
            'elections_past': elections_past
        }

        return Response(stats)

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Obtenir les élections à venir"""
        upcoming_elections = [obj for obj in self.get_queryset() if obj.is_upcoming]
        serializer = CalendrierElectoralUpcomingSerializer(upcoming_elections, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def today(self, request):
        """Obtenir les élections d'aujourd'hui"""
        today_elections = [obj for obj in self.get_queryset() if obj.is_today]
        serializer = self.get_serializer(today_elections, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_status(self, request):
        """Obtenir les élections par statut"""
        status_param = request.query_params.get('status')
        if not status_param:
            return Response(
                {'error': 'Paramètre status requis'},
                status=status.HTTP_400_BAD_REQUEST
            )

        elections = self.get_queryset().filter(status=status_param)
        serializer = self.get_serializer(elections, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Obtenir les élections récentes (dernières 24h)"""
        recent_elections = [obj for obj in self.get_queryset() if obj.is_recent]
        serializer = self.get_serializer(recent_elections, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Obtenir les élections par type"""
        type_id = request.query_params.get('type_id')
        if not type_id:
            return Response(
                {'error': 'Paramètre type_id requis'},
                status=status.HTTP_400_BAD_REQUEST
            )

        elections = self.get_queryset().filter(type_election_id=type_id)
        serializer = self.get_serializer(elections, many=True)
        return Response(serializer.data)


# Vues fonction pour l'interface web (optionnel)

def calendrier_electoral_list(request):
    """Vue pour afficher la liste du calendrier électoral"""
    elections = CalendrierElectoral.objects.select_related('type_election').all().order_by('-date')

    # Pagination
    paginator = Paginator(elections, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'total_elections': elections.count(),
        'upcoming_elections': len([obj for obj in elections if obj.is_upcoming])
    }

    return render(request, 'calendrier_electoral/list.html', context)


def calendrier_electoral_detail(request, pk):
    """Vue pour afficher le détail d'une élection"""
    election = get_object_or_404(CalendrierElectoral, pk=pk)

    context = {
        'election': election
    }

    return render(request, 'calendrier_electoral/detail.html', context)


@csrf_exempt
@require_http_methods(["GET"])
def calendrier_electoral_api_list(request):
    """API simple pour obtenir la liste du calendrier électoral"""
    try:
        elections = CalendrierElectoral.objects.select_related('type_election').all().order_by('-date')

        # Pagination simple
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 20))
        offset = (page - 1) * limit

        paginated_elections = elections[offset:offset + limit]

        data = []
        for election in paginated_elections:
            data.append({
                'id': election.id,
                'type_election': {
                    'id': election.type_election.id,
                    'name': election.type_election.name
                },
                'date': election.date.isoformat(),
                'status': election.status,
                'status_display': election.get_status_display(),
                'status_color': election.status_color,
                'is_past': election.is_past,
                'is_today': election.is_today,
                'is_upcoming': election.is_upcoming,
                'days_until_election': election.days_until_election,
                'is_recent': election.is_recent,
                'created_at': election.created_at.isoformat(),
                'updated_at': election.updated_at.isoformat()
            })

        return JsonResponse({
            'success': True,
            'data': data,
            'total': elections.count(),
            'page': page,
            'limit': limit
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def calendrier_electoral_api_create(request):
    """API simple pour créer une nouvelle élection au calendrier"""
    try:
        data = json.loads(request.body)

        # Validation de la date
        date_str = data.get('date')
        if not date_str:
            return JsonResponse({
                'success': False,
                'error': 'Date requise'
            }, status=400)

        try:
            date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except ValueError:
            return JsonResponse({
                'success': False,
                'error': 'Format de date invalide'
            }, status=400)

        election = CalendrierElectoral.objects.create(
            type_election_id=data.get('type_election'),
            date=date_obj,
            status=data.get('status', 'planifie')
        )

        return JsonResponse({
            'success': True,
            'data': {
                'id': election.id,
                'type_election': {
                    'id': election.type_election.id,
                    'name': election.type_election.name
                },
                'date': election.date.isoformat(),
                'status': election.status,
                'status_display': election.get_status_display(),
                'days_until_election': election.days_until_election,
                'created_at': election.created_at.isoformat()
            }
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
