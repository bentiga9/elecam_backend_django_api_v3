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
from .models import PickupPoint
from .serializers import PickupPointSerializer


class PickupPointViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les points de retrait via API REST
    GET: Accès libre, POST/PUT/DELETE: Authentification requise
    """
    queryset = PickupPoint.objects.all()
    serializer_class = PickupPointSerializer

    def get_permissions(self):
        """
        Permissions en fonction de la méthode HTTP
        GET: Libre accès
        POST/PUT/DELETE: Authentification requise
        """
        if self.action in ['list', 'retrieve', 'by_location', 'recent', 'types', 'count_pickup_points', 'count_voting_offices']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """Filtrage et recherche personnalisée"""
        queryset = PickupPoint.objects.all()

        # Filtrage par type
        point_type = self.request.query_params.get('type')
        if point_type:
            queryset = queryset.filter(type=point_type)

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
    def by_location(self, request):
        """Action personnalisée pour obtenir les points par zone géographique"""
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

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Obtenir les points de retrait récents (dernières 24h)"""
        recent_points = [obj for obj in self.get_queryset() if obj.is_recent]
        serializer = self.get_serializer(recent_points, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def types(self, request):
        """Obtenir la liste des types de points disponibles"""
        types = PickupPoint.objects.values_list('type', flat=True).distinct()
        return Response({'types': list(types)})

    @action(detail=False, methods=['get'])
    def count_pickup_points(self, request):
        """Compter uniquement les points de retrait (pickup_point)"""
        pickup_total = PickupPoint.objects.count()

        return Response({
            'nombre': pickup_total
        })

    @action(detail=False, methods=['get'])
    def count_voting_offices(self, request):
        """Compter uniquement les bureaux de vote (voting_office)"""
        from voting_office.models import VotingOffice

        voting_total = VotingOffice.objects.count()

        return Response({
            'nombre': voting_total
        })


# Vues fonction pour l'interface web (optionnel)

def pickup_point_list(request):
    """Vue pour afficher la liste des points de retrait"""
    points = PickupPoint.objects.all().order_by('-created_at')

    # Pagination
    paginator = Paginator(points, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'total_points': points.count()
    }

    return render(request, 'pickup_point/list.html', context)


def pickup_point_detail(request, pk):
    """Vue pour afficher le détail d'un point de retrait"""
    point = get_object_or_404(PickupPoint, pk=pk)

    context = {
        'point': point
    }

    return render(request, 'pickup_point/detail.html', context)


@csrf_exempt
@require_http_methods(["GET"])
def pickup_point_api_list(request):
    """API simple pour obtenir la liste des points de retrait"""
    try:
        points = PickupPoint.objects.all().order_by('-created_at')

        # Pagination simple
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 20))
        offset = (page - 1) * limit

        paginated_points = points[offset:offset + limit]

        data = []
        for point in paginated_points:
            data.append({
                'id': point.id,
                'name': point.name,
                'description': point.description,
                'nombre': point.nombre,
                'latitude': float(point.latitude),
                'longitude': float(point.longitude),
                'type': point.type,
                'coordinates': point.coordinates,
                'is_recent': point.is_recent,
                'created_at': point.created_at.isoformat(),
                'updated_at': point.updated_at.isoformat()
            })

        return JsonResponse({
            'success': True,
            'data': data,
            'total': points.count(),
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
def pickup_point_api_create(request):
    """API simple pour créer un nouveau point de retrait"""
    try:
        data = json.loads(request.body)

        point = PickupPoint.objects.create(
            name=data.get('name', ''),
            description=data.get('description', ''),
            nombre=data.get('nombre', ''),
            latitude=data.get('latitude', 0.0),
            longitude=data.get('longitude', 0.0),
            type=data.get('type', 'pickup_point')
        )

        return JsonResponse({
            'success': True,
            'data': {
                'id': point.id,
                'name': point.name,
                'description': point.description,
                'nombre': point.nombre,
                'latitude': float(point.latitude),
                'longitude': float(point.longitude),
                'type': point.type,
                'coordinates': point.coordinates,
                'created_at': point.created_at.isoformat()
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
