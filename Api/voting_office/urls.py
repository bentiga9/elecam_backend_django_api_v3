from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Configuration du router pour l'API REST
router = DefaultRouter()
router.register(r'', views.VotingOfficeViewSet, basename='voting-office')

app_name = 'voting_office'

urlpatterns = [
    # API REST avec Django REST Framework (endpoint principal)
    path('', include(router.urls)),

    # API simple avec vues fonction
    path('simple/list/', views.voting_office_api_list, name='api-list'),
    path('simple/create/', views.voting_office_api_create, name='api-create'),

    # Vues web (optionnel)
    path('web/', views.voting_office_list, name='list'),
    path('web/<int:pk>/', views.voting_office_detail, name='detail'),
]