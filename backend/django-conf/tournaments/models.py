from django.db import models
from django.core.validators import MinValueValidator

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