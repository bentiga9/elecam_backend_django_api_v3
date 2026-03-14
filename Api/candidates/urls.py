from django.urls import path
from . import views

urlpatterns = [
    path('', views.CandidatListCreateView.as_view(), name='candidat-list-create'),
    path('<int:pk>/', views.CandidatDetailView.as_view(), name='candidat-detail'),
]