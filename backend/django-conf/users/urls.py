from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import LoginView
from .views import LoginView, RegisterView

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
]