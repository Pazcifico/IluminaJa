from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import render
from django.views.generic import FormView, CreateView, ListView, UpdateView, DeleteView
from usuarios.models import PerfilUsuario

User = get_user_model()


class LoginView(FormView):
    template_name = 'contas/login.html'
    success_url = reverse_lazy('usuarios:lista_usuarios')

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        try:
            username = User.objects.get(email=email).username
        except User.DoesNotExist:
            messages.error(request, 'Usuário não encontrado.')
            return self.form_invalid(None)

        user = authenticate(request, username=username, password=senha)
        if user is not None:
            login(request, user)
            return redirect(self.get_success_url())
        else:
            messages.error(request, 'Senha incorreta.')
            return self.form_invalid(None)

    def get(self, request, *args, **kwargs):
        return self.render_to_response({})


class CadastroView(CreateView):
    model = User
    template_name = 'contas/cadastro.html'
    fields = ['first_name', 'email', 'password']
    success_url = reverse_lazy('usuarios:login')

    def post(self, request, *args, **kwargs):
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este e-mail já está cadastrado.')
            return redirect('usuarios:cadastro')

        usuario = User.objects.create_user(
            username=email,
            email=email,
            password=senha,
            first_name=nome
        )
        usuario.save()
        messages.success(request, 'Conta criada com sucesso! Faça login.')
        return redirect(self.success_url)


class LogoutView(LoginRequiredMixin, DjangoLogoutView):
    next_page = reverse_lazy('usuarios:login')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "Você saiu da sua conta.")
        return super().dispatch(request, *args, **kwargs)


class ListaUsuariosView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'usuarios/lista.html'
    context_object_name = 'usuarios'

    def get_queryset(self):
        busca = self.request.GET.get('busca', '')
        if busca:
            return User.objects.filter(
                Q(first_name__icontains=busca) | Q(email__icontains=busca)
            )
        return User.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['busca'] = self.request.GET.get('busca', '')
        return context


class EditarUsuarioView(LoginRequiredMixin, View):
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        perfil, _ = PerfilUsuario.objects.get_or_create(user=user)

        old_nome = user.first_name
        old_email = user.email
        old_tipo_tecnico = perfil.tipo_tecnico

        novo_nome = request.POST.get('nome')
        novo_email = request.POST.get('email')
        novo_tipo_tecnico = request.POST.get('tipo_tecnico')

        user.first_name = novo_nome
        user.email = novo_email
        user.save()

        perfil.tipo_tecnico = novo_tipo_tecnico
        perfil.save()

        mudanças = []
        if old_nome != novo_nome:
            mudanças.append(f"Nome: '{old_nome}' → '{novo_nome}'")
        if old_email != novo_email:
            mudanças.append(f"Email: '{old_email}' → '{novo_email}'")
        if old_tipo_tecnico != novo_tipo_tecnico:
            mudanças.append(
                f"Tipo Técnico: '{old_tipo_tecnico}' → '{novo_tipo_tecnico}'"
            )

        if mudanças:
            messages.success(
                request, "Usuário atualizado com sucesso: " +
                ", ".join(mudanças)
            )
        else:
            messages.info(request, "Nenhuma alteração feita.")

        return redirect('usuarios:lista_usuarios')


class ExcluirUsuarioView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    success_url = reverse_lazy('usuarios:lista_usuarios')

    def test_func(self):
        return self.request.user.is_superuser

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Usuário excluído com sucesso.")
        return super().delete(request, *args, **kwargs)


class PerfilUsuarioView(LoginRequiredMixin, View):
    template_name = 'usuarios/perfil.html'

    def get(self, request):
        perfil = getattr(request.user, 'perfilusuario', None)
        return render(request, self.template_name, {
            'usuario': request.user,
            'perfil': perfil,
        })

    def post(self, request):
        user = request.user
        perfil = getattr(user, 'perfilusuario', None)

        nome = request.POST.get('nome')
        email = request.POST.get('email')

        user.first_name = nome
        user.email = email
        user.save()

        senha_atual = request.POST.get('senha_atual')
        nova_senha = request.POST.get('nova_senha')
        confirma_senha = request.POST.get('confirma_senha')

        if senha_atual or nova_senha or confirma_senha:
            if not user.check_password(senha_atual):
                messages.error(request, 'Senha atual incorreta.')
            elif nova_senha != confirma_senha:
                messages.error(request, 'As senhas novas não conferem.')
            elif not nova_senha:
                messages.error(request, 'Informe a nova senha.')
            else:
                user.set_password(nova_senha)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Senha alterada com sucesso!')
        else:
            messages.success(request, 'Perfil atualizado com sucesso!')

        return redirect('usuarios:perfil')
