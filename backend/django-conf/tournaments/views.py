from django.shortcuts import render

from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .models import Tournament
from .serializers import TournamentSerializer
from .permissions import IsAdminRoleOrReadOnly

# Налаштовуємо базову пагінацію
class TournamentPagination(PageNumberPagination):
    page_size = 10  # Кількість турнірів на одній сторінці за замовчуванням
    page_size_query_param = 'limit'  # Дозволяє клієнту змінювати ліміт через ?limit=5
    max_page_size = 50

# endpoints for GET (list) and POST (creation)
class TournamentListCreateView(generics.ListCreateAPIView):
    serializer_class = TournamentSerializer
    permission_classes = [IsAdminRoleOrReadOnly]
    pagination_class = TournamentPagination  # Підключаємо пагінацію сюди

    def get_queryset(self):
        # Беремо всі турніри, сортуємо від найновіших (за ID або start_date)
        queryset = Tournament.objects.all().order_by('-id')
        
        # Перевіряємо, чи користувач є Адміном
        is_admin = bool(
            self.request.user and 
            self.request.user.is_authenticated and 
            getattr(self.request.user, 'role', '') == 'admin'
        )

        # 2. Логіка приховування Draft
        # Якщо це НЕ адмін, виключаємо всі турніри зі статусом Draft
        if not is_admin:
            queryset = queryset.exclude(status='Draft')

        # 3. Підтримка query-параметрів для фільтрації (?status=Running)
        status_param = self.request.query_params.get('status')
        if status_param:
            # Запобіжник: якщо звичайний юзер намагається хитрощами витягнути Draft
            if status_param == 'Draft' and not is_admin:
                return queryset.none()  # Повертаємо порожній список
            
            queryset = queryset.filter(status=status_param)

        return queryset

# endpoint for GET, PUT, PATCH, DELETE tournament by ID
class TournamentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = [IsAdminRoleOrReadOnly]