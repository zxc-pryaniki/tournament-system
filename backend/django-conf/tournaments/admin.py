from django.contrib import admin
from .models import Tournament, Team, Participant, User

# Додаємо наші таблиці в адмін-панель
admin.site.register(Tournament)
admin.site.register(Team)
admin.site.register(Participant)
admin.site.register(User)