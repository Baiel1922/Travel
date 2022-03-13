from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ValidationError

from account.models import User
from account.utils import send_activation_code

User = get_user_model()


class RegistrationSerializer(ModelSerializer):
    password = serializers.CharField(min_length=8, required=True)
    password_confirm = serializers.CharField(min_length=8, required=True)
    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirm')

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "Пользователь с таким email уже зарегестрирован"
            )
        return email

    def validate(self, data):
        password = data.get('password')
        password_confirm = data.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError(
                "Пароли должны совпадать"
            )
        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.create_activation_code()
        send_activation_code(user.email, user.activation_code)
        return user


class ActivationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True)

    def validate(self, data):
        email = data.get('email')
        code = data.get('code')
        if not User.objects.filter(email=email, activation_code=code).exists():
            raise serializers.ValidationError("Пользователь не найден")
        return data

    def activate(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        # получение одной записи с бд
        user.is_active = True
        user.activation_code = ''
        user.save()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Пользователь с таким email не найден")
        return email

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        request = self.context.get('request')
        if email and password:
            user = authenticate(username=email, password=password, request=request)
            if not user:
                raise serializers.ValidationError("Неверный email или пароль")
        else:
            raise serializers.ValidationError("email и пароль обязательны к заполнению")
        data['user'] = user
        return data