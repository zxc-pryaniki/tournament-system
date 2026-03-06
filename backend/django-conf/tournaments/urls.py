from django.urls import path
from .views import TournamentListCreateView, TournamentDetailView

urlpatterns = [
    # POST /api/tournaments/ (і GET для списку)
    path('tournaments/', TournamentListCreateView.as_view(), name='tournament-list-create'),
    
    # PUT /api/tournaments/<id>/ (і GET, DELETE для конкретного)
    path('tournaments/<int:pk>/', TournamentDetailView.as_view(), name='tournament-detail'),
]