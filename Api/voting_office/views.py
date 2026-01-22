from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
import json
from .models import VotingOffice
from .serializers import VotingOfficeSerializer


class VotingOfficeViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les bureaux de vote via API REST
    GET: Accès libre, POST/PUT/DELETE: Authentification requise
    """
    queryset = VotingOffice.objects.all()
    serializer_class = VotingOfficeSerializer

    def get_permissions(self):
        """
        Permissions en fonction de la méthode HTTP
        GET: Libre accès
        POST/PUT/DELETE: Authentification requise
        """
        if self.action in ['list', 'retrieve', 'statistics', 'active', 'inactive', 'recent', 'by_location']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """Filtrage et recherche personnalisée"""
        queryset = VotingOffice.objects.all()

        # Filtrage par statut actif/inactif
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')

        # Filtrage par plage de dates
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        if date_from:
            queryset = queryset.filter(created_at__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__lte=date_to)

        # Recherche textuelle
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(nombre__icontains=search)
            )

        return queryset.order_by('-created_at')

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Action personnalisée pour obtenir des statistiques"""
        queryset = self.get_queryset()
        total = queryset.count()

        if total == 0:
            return Response({
                'total_offices': 0,
                'active_offices': 0,
                'inactive_offices': 0,
                'recent_offices': 0,
                'activity_rate': 0.0
            })

        active = queryset.filter(is_active=True).count()
        inactive = queryset.filter(is_active=False).count()
        recent = len([obj for obj in queryset if obj.is_recent])
        activity_rate = round((active / total) * 100, 2) if total > 0 else 0.0

        stats = {
            'total_offices': total,
            'active_offices': active,
            'inactive_offices': inactive,
            'recent_offices': recent,
            'activity_rate': activity_rate
        }

        return Response(stats)

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Obtenir uniquement les bureaux de vote actifs"""
        active_offices = self.get_queryset().filter(is_active=True)
        serializer = self.get_serializer(active_offices, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def inactive(self, request):
        """Obtenir uniquement les bureaux de vote inactifs"""
        inactive_offices = self.get_queryset().filter(is_active=False)
        serializer = self.get_serializer(inactive_offices, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Obtenir les bureaux de vote récents (dernières 24h)"""
        recent_offices = [obj for obj in self.get_queryset() if obj.is_recent]
        serializer = self.get_serializer(recent_offices, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_location(self, request):
        """Action personnalisée pour obtenir les bureaux par zone géographique"""
        queryset = self.get_queryset()

        # Filtrage par coordonnées (zone géographique)
        lat_min = request.query_params.get('lat_min')
        lat_max = request.query_params.get('lat_max')
        lng_min = request.query_params.get('lng_min')
        lng_max = request.query_params.get('lng_max')

        if lat_min and lat_max and lng_min and lng_max:
            try:
                queryset = queryset.filter(
                    latitude__gte=float(lat_min),
                    latitude__lte=float(lat_max),
                    longitude__gte=float(lng_min),
                    longitude__lte=float(lng_max)
                )
            except ValueError:
                return Response(
                    {'error': 'Coordonnées invalides'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# Vues fonction pour l'interface web (optionnel)

def voting_office_list(request):
    """Vue pour afficher la liste des bureaux de vote"""
    offices = VotingOffice.objects.all().order_by('-created_at')

    # Pagination
    paginator = Paginator(offices, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'total_offices': offices.count(),
        'active_offices': offices.filter(is_active=True).count()
    }

    return render(request, 'voting_office/list.html', context)


def voting_office_detail(request, pk):
    """Vue pour afficher le détail d'un bureau de vote"""
    office = get_object_or_404(VotingOffice, pk=pk)

    context = {
        'office': office
    }

    return render(request, 'voting_office/detail.html', context)


@csrf_exempt
@require_http_methods(["GET"])
def voting_office_api_list(request):
    """API simple pour obtenir la liste des bureaux de vote"""
    try:
        offices = VotingOffice.objects.all().order_by('-created_at')

        # Pagination simple
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 20))
        offset = (page - 1) * limit

        paginated_offices = offices[offset:offset + limit]

        data = []
        for office in paginated_offices:
            data.append({
                'id': office.id,
                'name': office.name,
                'description': office.description,
                'nombre': office.nombre,
                'latitude': float(office.latitude),
                'longitude': float(office.longitude),
                'is_active': office.is_active,
                'coordinates': office.coordinates,
                'is_recent': office.is_recent,
                'status_display': office.status_display,
                'created_at': office.created_at.isoformat(),
                'updated_at': office.updated_at.isoformat()
            })

        return JsonResponse({
            'success': True,
            'data': data,
            'total': offices.count(),
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
def voting_office_api_create(request):
    """API simple pour créer un nouveau bureau de vote"""
    try:
        data = json.loads(request.body)

        office = VotingOffice.objects.create(
            name=data.get('name', ''),
            description=data.get('description', ''),
            nombre=data.get('nombre', ''),
            latitude=data.get('latitude', 0.0),
            longitude=data.get('longitude', 0.0),
            is_active=data.get('is_active', True)
        )

        return JsonResponse({
            'success': True,
            'data': {
                'id': office.id,
                'name': office.name,
                'description': office.description,
                'nombre': office.nombre,
                'latitude': float(office.latitude),
                'longitude': float(office.longitude),
                'is_active': office.is_active,
                'coordinates': office.coordinates,
                'status_display': office.status_display,
                'created_at': office.created_at.isoformat()
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
