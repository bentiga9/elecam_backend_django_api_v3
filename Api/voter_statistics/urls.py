from django.urls import path
from .views import VoterStatisticsListCreateAPIView, VoterStatisticsDetailAPIView

app_name = 'voter_statistics'

urlpatterns = [
    path('', VoterStatisticsListCreateAPIView.as_view(), name='list-create'),
    path('<int:pk>/', VoterStatisticsDetailAPIView.as_view(), name='detail'),
]