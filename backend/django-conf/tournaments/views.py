from django.shortcuts import render
from rest_framework import generics
from .models import Tournament
from .serializers import TournamentSerializer
from .permissions import IsAdminRoleOrReadOnly

# endpoints for GET (list) and POST (creation)
class TournamentListCreateView(generics.ListCreateAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = [IsAdminRoleOrReadOnly]

# endpoint for GET, PUT, PATCH, DELETE tournament by ID
class TournamentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = [IsAdminRoleOrReadOnly]