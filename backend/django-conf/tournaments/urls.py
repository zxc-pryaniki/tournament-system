from django.urls import path
from .views import TournamentListCreateView, TournamentDetailView
from .views import TeamRegisterView

urlpatterns = [
    # POST /api/tournaments/ (і GET для списку)
    path('tournaments/', TournamentListCreateView.as_view(), name='tournament-list-create'),
    
    # PUT /api/tournaments/<id>/ (і GET, DELETE для конкретного)
    path('tournaments/<int:pk>/', TournamentDetailView.as_view(), name='tournament-detail'),

    path('tournaments/<int:tournamentId>/teams/', TeamRegisterView.as_view(), name='team-register'),
]