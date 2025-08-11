from django.urls import path
from .views import (
    LoginView, CadastroView, LogoutView,
    ListaUsuariosView, EditarUsuarioView,
    ExcluirUsuarioView, PerfilUsuarioView
)

app_name = 'usuarios'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('cadastro/', CadastroView.as_view(), name='cadastro'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('lista/', ListaUsuariosView.as_view(), name='lista_usuarios'),
    path('editar/<int:user_id>/', EditarUsuarioView.as_view(), name='editar_usuario'),
    path('excluir/<int:pk>/', ExcluirUsuarioView.as_view(), name='excluir_usuario'),
    path('perfil/', PerfilUsuarioView.as_view(), name='perfil'),
]
