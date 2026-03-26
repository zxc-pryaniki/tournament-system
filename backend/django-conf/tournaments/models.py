from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()

class Tournament(models.Model):
    STATUS_CHOICES = [
        ('Draft', 'Draft'),
        ('Registration', 'Registration'),
        ('Running', 'Running'),
        ('Finished', 'Finished'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    # reg window
    registration_start = models.DateTimeField()
    registration_end = models.DateTimeField()
    
    # date of start tournm
    start_date = models.DateTimeField(blank=True, null=True)
    
    max_teams = models.PositiveIntegerField(blank=True, null=True)
    number_of_rounds = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Draft')

    def __str__(self):
        return self.title
    

class Team(models.Model):
    tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE, related_name='teams')
    captain = models.ForeignKey(User, on_delete=models.CASCADE, related_name='captained_teams')
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255, blank=True, null=True)
    telegram = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.tournament.title})"

class Participant(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='participants')
    full_name = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return f"{self.full_name} - {self.team.name}"