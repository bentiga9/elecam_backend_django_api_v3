from django.urls import path
from . import views

urlpatterns = [
    path('', views.PartiePolitiqueListCreateView.as_view(), name='partie-politique-list-create'),
    path('<int:pk>/', views.PartiePolitiqueDetailView.as_view(), name='partie-politique-detail'),
]