from django.urls import path
from . import views

urlpatterns = [
    path('candidates/', views.CandidatListCreateView.as_view(), name='candidat-list-create'),
    path('candidates/<int:pk>/', views.CandidatDetailView.as_view(), name='candidat-detail'),
]