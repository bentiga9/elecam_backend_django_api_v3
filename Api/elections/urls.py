from django.urls import path
from .views import (
    ElectionListCreateAPIView, 
    ElectionDetailAPIView,
    election_statistics
)

app_name = 'elections'  # Namespace pour les URLs

urlpatterns = [
    # CRUD de base pour les élections
    path('', ElectionListCreateAPIView.as_view(), name='list-create'),
    path('<int:pk>/', ElectionDetailAPIView.as_view(), name='detail'),

    # Endpoint additionnel pour les statistiques
    path('statistics/', election_statistics, name='statistics'),
]