from django.urls import path
from . import views

urlpatterns = [
    path('parties/', views.PartiePolitiqueListCreateView.as_view(), name='partie-politique-list-create'),
    path('parties/<int:pk>/', views.PartiePolitiqueDetailView.as_view(), name='partie-politique-detail'),
]