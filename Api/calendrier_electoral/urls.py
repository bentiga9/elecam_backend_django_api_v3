from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Configuration du router pour l'API REST
router = DefaultRouter()
router.register(r'', views.CalendrierElectoralViewSet, basename='calendrier-electoral')

app_name = 'calendrier_electoral'

urlpatterns = [
    # API REST avec Django REST Framework (endpoint principal)
    path('', include(router.urls)),

    # API simple avec vues fonction
    path('simple/list/', views.calendrier_electoral_api_list, name='api-list'),
    path('simple/create/', views.calendrier_electoral_api_create, name='api-create'),

    # Vues web (optionnel)
    path('web/', views.calendrier_electoral_list, name='list'),
    path('web/<int:pk>/', views.calendrier_electoral_detail, name='detail'),
]