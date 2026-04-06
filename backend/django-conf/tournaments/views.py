from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from .models import Tournament, Team
from .serializers import (
    TournamentSerializer, 
    TeamCreateSerializer, 
    TeamUpdateSerializer
)
from .permissions import IsAdminRoleOrReadOnly, IsCaptainOrAdmin

# Налаштовуємо базову пагінацію
class TournamentPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 50

# Ендпоінт для GET (список) та POST (створення турніру)
class TournamentListCreateView(generics.ListCreateAPIView):
    serializer_class = TournamentSerializer
    permission_classes = [IsAdminRoleOrReadOnly]
    pagination_class = TournamentPagination

    def get_queryset(self):
        queryset = Tournament.objects.all().order_by('-id')
        
        is_admin = bool(
            self.request.user and 
            self.request.user.is_authenticated and 
            getattr(self.request.user, 'role', '') == 'admin'
        )

        # Приховуємо Draft для звичайних користувачів
        if not is_admin:
            queryset = queryset.exclude(status='Draft')

        # Фільтрація через query-параметри (?status=Running)
        status_param = self.request.query_params.get('status')
        if status_param:
            if status_param == 'Draft' and not is_admin:
                return queryset.none()
            queryset = queryset.filter(status=status_param)

        return queryset

# Ендпоінт для GET, PUT, PATCH, DELETE турніру за ID
class TournamentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = [IsAdminRoleOrReadOnly]

# Ендпоінт для реєстрації команди (POST)
class TeamRegisterView(generics.CreateAPIView):
    serializer_class = TeamCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        tournament_id = self.kwargs.get('tournamentId')
        # Передаємо турнір у серіалізатор для валідації дат
        context['tournament'] = get_object_or_404(Tournament, id=tournament_id)
        return context

    def perform_create(self, serializer):
        # Прив'язуємо команду до турніру та поточного юзера (капітана)
        tournament = self.get_serializer_context()['tournament']
        serializer.save(captain=self.request.user, tournament=tournament)

# Ендпоінт для оновлення команди (PUT/PATCH/GET/DELETE)
class TeamUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamUpdateSerializer
    # Використовуємо кастомний пермішн (Адмін або Капітан до дедлайну)
    permission_classes = [IsAuthenticated, IsCaptainOrAdmin]