from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone

class IsAdminRoleOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return bool(
            request.user and 
            request.user.is_authenticated and 
            getattr(request.user, 'role', '') == 'admin'
        )

class IsCaptainOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # 1. Перевірка на Адміна
        # Якщо роль користувача 'admin' — він проходить ЗАВЖДИ
        is_admin = (
            request.user.is_authenticated and 
            (getattr(request.user, 'is_staff', False) or getattr(request.user, 'role', '') == 'admin')
        )
        
        if is_admin:
            print(f"--- [DEBUG] Юзер {request.user.email} - АДМІН. Дедлайни ігноруються. ---")
            return True
            
        # 2. Перевірка на Капітана
        if obj.captain == request.user:
            now = timezone.now()
            tournament = obj.tournament
            
            print(f"--- [DEBUG] ПЕРЕВІРКА ДЕДЛАЙНУ ДЛЯ КАПІТАНА {request.user.email} ---")
            print(f"Зараз (UTC): {now}")
            print(f"Кінець реєстрації: {tournament.registration_end}")

            # Логічна умова: чи зараз час між початком і кінцем
            is_registration_open = tournament.registration_start <= now <= tournament.registration_end
            
            print(f"Реєстрація відкрита? {is_registration_open}")

            if not is_registration_open:
                print("--- [DEBUG] ВІДМОВА: Час реєстрації вичерпано. ---")
                raise PermissionDenied("Редагування після завершення реєстрації заборонено.")
            
            print("--- [DEBUG] ДОЗВОЛЕНО: Реєстрація ще триває. ---")
            return True
            
        print(f"--- [DEBUG] ВІДМОВА: Юзер {request.user.email} не є капітаном цієї команди. ---")
        return False