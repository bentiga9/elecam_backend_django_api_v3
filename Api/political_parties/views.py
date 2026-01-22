from rest_framework import generics, status
from rest_framework.response import Response
from .models import PartiePolitique
from .serializers import PartiePolitiqueSerializer

class PartiePolitiqueListCreateView(generics.ListCreateAPIView):
    queryset = PartiePolitique.objects.all()
    serializer_class = PartiePolitiqueSerializer

class PartiePolitiqueDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PartiePolitique.objects.all()
    serializer_class = PartiePolitiqueSerializer