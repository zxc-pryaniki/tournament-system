from rest_framework import serializers
from .models import Tournament, Team, Participant
from django.utils import timezone
from rest_framework.exceptions import ValidationError

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
    
class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ['full_name', 'email']

class TeamCreateSerializer(serializers.ModelSerializer):
    # Дозволяємо передавати масив об'єктів учасників
    participants = ParticipantSerializer(many=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'city', 'telegram', 'participants']
        read_only_fields = ['id']

    def validate(self, attrs):
        # Отримуємо турнір з контексту URL і юзера з токена
        tournament = self.context['tournament']
        user = self.context['request'].user
        participants_data = attrs.get('participants', [])

        # 1. Сувора перевірка часових рамок
        now = timezone.now()
        if not (tournament.registration_start <= now <= tournament.registration_end):
            raise ValidationError({"detail": "Реєстрація закрита або ще не розпочалась."})

        # 2. Перевірка кількості учасників (мінімум 2)
        if len(participants_data) < 2:
            raise ValidationError({"participants": "Команда повинна мати мінімум 2 учасників (окрім капітана)."})

        # 3. Захист від дублікатів у самому запиті (включаючи капітана)
        emails_in_request = [p['email'] for p in participants_data]
        emails_in_request.append(user.email) # Додаємо email капітана
        
        if len(set(emails_in_request)) != len(emails_in_request):
            raise ValidationError({"participants": "У списку учасників є однакові email-адреси (або email збігається з капітаном)."})

        # 4. Перевірка по базі даних (чи є ці email-и ВЖЕ на цьому ж турнірі)
        # Шукаємо серед звичайних учасників
        existing_participants = Participant.objects.filter(
            team__tournament=tournament, 
            email__in=emails_in_request
        ).values_list('email', flat=True)
        
        # Шукаємо серед капітанів інших команд цього турніру
        existing_captains = Team.objects.filter(
            tournament=tournament, 
            captain__email__in=emails_in_request
        ).values_list('captain__email', flat=True)

        conflict_emails = set(existing_participants) | set(existing_captains)
        if conflict_emails:
            raise ValidationError({
                "participants": f"Ці учасники вже зареєстровані на цей турнір: {', '.join(conflict_emails)}"
            })

        return attrs

    def create(self, validated_data):
        # Витягуємо учасників, щоб зберегти їх окремо
        participants_data = validated_data.pop('participants')
        
        # Призначаємо турнір та капітана (з контексту)
        validated_data['tournament'] = self.context['tournament']
        validated_data['captain'] = self.context['request'].user
        
        # Створюємо команду
        team = Team.objects.create(**validated_data)
        
        # Створюємо всіх учасників за один запит до БД (оптимізація)
        Participant.objects.bulk_create([
            Participant(team=team, **p_data) for p_data in participants_data
        ])
        
        return team