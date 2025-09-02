from rest_framework import viewsets, permissions
from .models import Manutencao
from .serializers import ManutencaoSerializer


class ManutencaoViewSet(viewsets.ModelViewSet):
    queryset = Manutencao.objects.all().order_by('-data_manutencao')
    serializer_class = ManutencaoSerializer
    permission_classes = [permissions.IsAuthenticated]
