from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('jury', 'Jury'),
        ('team', 'Team'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='team')

    def __str__(self):
        return f"{self.username} ({self.role})"
