from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Configuration du router pour l'API REST
router = DefaultRouter()
router.register(r'', views.PickupPointViewSet, basename='pickup-point')

app_name = 'pickup_point'

urlpatterns = [
    # API REST avec Django REST Framework (endpoint principal)
    path('', include(router.urls)),

    # API simple avec vues fonction
    path('simple/list/', views.pickup_point_api_list, name='api-list'),
    path('simple/create/', views.pickup_point_api_create, name='api-create'),

    # Vues web (optionnel)
    path('web/', views.pickup_point_list, name='list'),
    path('web/<int:pk>/', views.pickup_point_detail, name='detail'),
]