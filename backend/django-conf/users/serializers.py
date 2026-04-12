from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, ValidationError 
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





class RegisterSerializer(serializers.ModelSerializer):
    fullName = serializers.CharField(write_only=True, required=True)
    
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        min_length=6,
        error_messages={
            'min_length': 'Пароль має містити мінімум 6 символів.',
            'blank': "Це поле є обов'язковим."
        }
    )

    class Meta:
        model = User
        fields = ('email', 'password', 'fullName')

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("Користувач з таким email вже існує")
        return value

    def create(self, validated_data):
        name_parts = validated_data['fullName'].split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ""

        user = User.objects.create_user(
            username=validated_data['email'], 
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=first_name,
            last_name=last_name
        )

      
        if hasattr(user, 'role'):
            user.role = 'Team'
            user.save()

        return user