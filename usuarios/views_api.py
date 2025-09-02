from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from .serializers import UsuarioSerializer
from .models import PerfilUsuario

User = get_user_model()


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]
