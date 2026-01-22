from django.urls import path
from .views import ElectionTypeListCreateAPIView, ElectionTypeDetailAPIView

app_name = 'election_types'

urlpatterns = [
    path('', ElectionTypeListCreateAPIView.as_view(), name='list-create'),
    path('<int:pk>/', ElectionTypeDetailAPIView.as_view(), name='detail'),
]