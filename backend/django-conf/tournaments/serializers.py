from rest_framework import serializers
from .models import Tournament

class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = '__all__'

    def validate(self, data):
        # Логіка: якщо start_date не передано, беремо registration_start
        if not data.get('start_date') and data.get('registration_start'):
            data['start_date'] = data['registration_start']
            
        # Додаткова валідація: дата завершення реєстрації має бути після початку
        if data.get('registration_end') and data.get('registration_start'):
            if data['registration_end'] <= data['registration_start']:
                raise serializers.ValidationError({"registration_end": "Кінець реєстрації не може бути раніше її початку."})

        return data