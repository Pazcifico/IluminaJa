from django.urls import path
from . import views

app_name = 'cadastro_poste'

urlpatterns = [
    path('lampadas/', views.lista_lampadas, name='lista_lampadas'),
    path('lampadas/adicionar/', views.adicionar_lampada, name='adicionar_lampada'),
    path('lampadas/editar/<int:pk>/', views.editar_lampada, name='editar_lampada'),
    path('lampadas/excluir/<int:pk>/',
         views.excluir_lampada, name='excluir_lampada'),

    path('poste/cadastro/', views.cadastro_poste, name='cadastro_poste'),
    path('poste/endereco/', views.endereco_poste, name='endereco_poste'),
    path('poste/sucesso/', views.sucesso, name='sucesso'),
    path('postes/', views.lista_de_postes, name='lista_postes'),

    path('mapa/', views.mapa_view, name='mapa'),
    path('lampada/poste/<int:poste_id>/',
         views.lampada_por_poste, name='lampada_por_poste'),
]
