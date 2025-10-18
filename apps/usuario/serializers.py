from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id_usuario', 'nome', 'login', 'email',
                  'dt_inclusao', 'dt_alteracao', 'is_active', 'is_admin')
        read_only_fields = ('id_usuario', 'dt_inclusao', 'dt_alteracao')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        label='Confirmar senha'
    )

    class Meta:
        model = User
        fields = ('nome', 'login', 'email', 'password', 'password2')
        extra_kwargs = {
            'nome': {'required': True},
            'login': {'required': True},
            'email': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "As senhas não coincidem."
            })
        return attrs

    def validate_login(self, value):
        if User.objects.filter(login=value).exists():
            raise serializers.ValidationError("Este login já está em uso.")
        return value

    def validate_email(self, value):
        """Valida se o email já existe"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email já está em uso.")
        return value

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    login = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True,
        style={'input_type': 'password'},
        write_only=True
    )
