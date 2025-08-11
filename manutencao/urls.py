from django.urls import path
from .views import (
    ListaManutencoesView,
    CriarManutencaoView,
    EditarManutencaoView,
    ExcluirManutencaoView,
    RegistrarCorrecaoView,
)

app_name = 'manutencao'

urlpatterns = [
    path('', ListaManutencoesView.as_view(), name='lista_manutencoes'),
    path('criar/', CriarManutencaoView.as_view(), name='criar_manutencao'),
    path('editar/<int:pk>/', EditarManutencaoView.as_view(),
         name='editar_manutencao'),
    path('excluir/<int:pk>/', ExcluirManutencaoView.as_view(),
         name='excluir_manutencao'),
    path('registrar_correcao/', RegistrarCorrecaoView.as_view(),
         name='registrar_correcao'),
]
