from rest_framework import generics, filters, permissions
from .models import ElectionType
from .serializers import ElectionTypeSerializer
from .permissions import AdminWriteOnlyPermission


class ElectionTypeListCreateAPIView(generics.ListCreateAPIView):
    """
    Liste et création de types d'élections.
    """
    queryset = ElectionType.objects.all()
    serializer_class = ElectionTypeSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name']
    ordering = ['name']
    permission_classes = [AdminWriteOnlyPermission]


class ElectionTypeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Détail, mise à jour et suppression d'un type d'élection.
    """
    queryset = ElectionType.objects.all()
    serializer_class = ElectionTypeSerializer
    permission_classes = [AdminWriteOnlyPermission]