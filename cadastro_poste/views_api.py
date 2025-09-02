from rest_framework import viewsets, permissions
from .models import Poste, Lampada
from .serializers import PosteSerializer, LampadaSerializer


class PosteViewSet(viewsets.ModelViewSet):
    queryset = Poste.objects.all()
    serializer_class = PosteSerializer
    permission_classes = [permissions.IsAuthenticated]


class LampadaViewSet(viewsets.ModelViewSet):
    queryset = Lampada.objects.all()
    serializer_class = LampadaSerializer
    permission_classes = [permissions.IsAuthenticated]
