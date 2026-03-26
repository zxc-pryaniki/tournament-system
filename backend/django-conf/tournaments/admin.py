from django.contrib import admin
from .models import Tournament, Team, Participant

# Додаємо наші таблиці в адмін-панель
admin.site.register(Tournament)
admin.site.register(Team)
admin.site.register(Participant)