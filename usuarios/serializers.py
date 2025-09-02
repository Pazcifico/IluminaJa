from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import PerfilUsuario

User = get_user_model()


class PerfilUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilUsuario
        fields = ['tipo_tecnico']


class UsuarioSerializer(serializers.ModelSerializer):
    perfilusuario = PerfilUsuarioSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'email', 'perfilusuario']
