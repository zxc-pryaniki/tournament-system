from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from .models import Tournament, Team, Participant

class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = '__all__'

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ['full_name', 'email']

class TeamCreateSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'city', 'telegram', 'participants']

    def validate(self, attrs):
        # Отримуємо турнір з контексту, який ми передали у View
        tournament = self.context.get('tournament')
        if not tournament:
            raise ValidationError("Турнір не знайдено в контексті.")

        now = timezone.now()
        # Перевірка вікна реєстрації
        if not (tournament.registration_start <= now <= tournament.registration_end):
            raise ValidationError("Реєстрація на цей турнір закрита або ще не почалася.")

        participants_data = attrs.get('participants', [])
        if len(participants_data) < 2:
            raise ValidationError({"participants": "Команда повинна мати мінімум 2 учасників."})

        # Перевірка унікальності email (включаючи капітана)
        user_email = self.context['request'].user.email
        emails_in_req = [p['email'] for p in participants_data] + [user_email]
        
        if len(set(emails_in_req)) != len(emails_in_req):
            raise ValidationError("Email-адреси у списку учасників та капітана повинні бути унікальними.")

        # Перевірка по базі даних
        existing_p = Participant.objects.filter(team__tournament=tournament, email__in=emails_in_req).exists()
        existing_c = Team.objects.filter(tournament=tournament, captain__email__in=emails_in_req).exists()

        if existing_p or existing_c:
            raise ValidationError("Один або декілька учасників вже зареєстровані на цей турнір.")

        return attrs

    def create(self, validated_data):
        participants_data = validated_data.pop('participants')
        team = Team.objects.create(**validated_data)
        
        # Створюємо учасників через bulk_create
        Participant.objects.bulk_create([
            Participant(team=team, **p_data) for p_data in participants_data
        ])
        return team

class TeamUpdateSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'city', 'telegram', 'participants']
        read_only_fields = ['id']

    def validate(self, attrs):
        team = self.instance 
        tournament = team.tournament
        participants_data = attrs.get('participants', [])

        if len(participants_data) < 2:
            raise ValidationError({"participants": "Команда повинна мати мінімум 2 учасників."})

        # Перевірка унікальності (виключаючи поточну команду, щоб не конфліктувати з самим собою)
        emails_in_req = [p['email'] for p in participants_data] + [team.captain.email]
        
        if len(set(emails_in_req)) != len(emails_in_req):
            raise ValidationError("Email-адреси дублюються в запиті.")

        exists_p = Participant.objects.filter(
            team__tournament=tournament, email__in=emails_in_req
        ).exclude(team=team).exists()
        
        exists_c = Team.objects.filter(
            tournament=tournament, captain__email__in=emails_in_req
        ).exclude(id=team.id).exists()

        if exists_p or exists_c:
            raise ValidationError("Ці учасники вже зареєстровані в інших командах на цей турнір.")

        return attrs

    def update(self, instance, validated_data):
        participants_data = validated_data.pop('participants', None)
        
        # Оновлюємо поля самої команди
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Повне оновлення списку учасників
        if participants_data is not None:
            instance.participants.all().delete()
            Participant.objects.bulk_create([
                Participant(team=instance, **p_data) for p_data in participants_data
            ])
        return instance