from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        error_messages={
            "invalid": "Введіть коректну email адресу.",
            "blank": "Це поле є обов'язковим.",
            "required": "Це поле є обов'язковим."
        }
    )
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        error_messages={
            "blank": "Це поле є обов'язковим.",
            "required": "Це поле є обов'язковим."
        }
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            # finding by email
            user = User.objects.get(email=email)
            user_auth = authenticate(username=user.username, password=password)
        except User.DoesNotExist:
            user_auth = None

        if not user_auth:
            # 401
            raise AuthenticationFailed("Bad credentials")

        # gen tkcn
        refresh = RefreshToken.for_user(user_auth)

        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }