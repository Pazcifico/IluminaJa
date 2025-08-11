from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseForbidden


from .models import Manutencao
from cadastro_poste.models import Poste, Lampada
from .forms import ManutencaoForm


class ListaManutencoesView(LoginRequiredMixin, ListView):
    model = Manutencao
    template_name = 'manutencao/lista.html'
    context_object_name = 'manutencoes'
    ordering = ['-data_manutencao']

    def get_queryset(self):
        queryset = super().get_queryset()
        busca = self.request.GET.get('busca', '')
        if busca:
            queryset = queryset.filter(
                Q(poste__id__icontains=busca) |
                Q(lampada__id__icontains=busca) |
                Q(tipo__icontains=busca) |
                Q(descricao__icontains=busca) |
                Q(status__icontains=busca) |
                Q(responsavel__username__icontains=busca)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['postes'] = Poste.objects.all()
        context['lampadas'] = Lampada.objects.all()
        context['busca'] = self.request.GET.get('busca', '')
        return context


class CriarManutencaoView(LoginRequiredMixin, CreateView):
    model = Manutencao
    form_class = ManutencaoForm
    template_name = 'manutencao/criar.html'
    success_url = reverse_lazy('manutencao:lista_manutencoes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipos'] = Manutencao.TIPO_MANUTENCAO_CHOICES
        context['status_choices'] = Manutencao.STATUS_CHOICES
        context['postes'] = Poste.objects.all()
        context['lampadas'] = Lampada.objects.all()
        return context

    def form_valid(self, form):
        manutencao = form.save(commit=False)
        manutencao.responsavel = self.request.user
        manutencao.save()
        messages.success(self.request, 'Manutenção cadastrada com sucesso.')
        return super().form_valid(form)


class EditarManutencaoView(LoginRequiredMixin, UpdateView):
    model = Manutencao
    form_class = ManutencaoForm
    template_name = 'manutencao/editar.html'
    success_url = reverse_lazy('manutencao:lista_manutencoes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['postes'] = Poste.objects.all()
        context['lampadas'] = Lampada.objects.all()
        return context

    def form_valid(self, form):
        manutencao_atualizado = form.save(commit=False)
        manutencao_atualizado.responsavel = self.get_object(
        ).responsavel
        manutencao_atualizado.save()
        return redirect(self.success_url)


class IsStaffMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return HttpResponseForbidden("Você não tem permissão para excluir manutenções.")


class ExcluirManutencaoView(LoginRequiredMixin, IsStaffMixin, DeleteView):
    model = Manutencao
    success_url = reverse_lazy('manutencao:lista_manutencoes')


class RegistrarCorrecaoView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        poste_id = request.POST.get('poste_id')
        lampada_id = request.POST.get('lampada_id')
        tipo = request.POST.get('tipo')
        descricao = request.POST.get('descricao')

        poste = get_object_or_404(Poste, id=poste_id)
        lampada = get_object_or_404(Lampada, id=lampada_id)

        Manutencao.objects.create(
            poste=poste,
            lampada=lampada,
            tipo=tipo,
            descricao=descricao,
            data_manutencao=timezone.now().date(),
            status='concluido',
            responsavel=request.user
        )

        poste.status = 3
        poste.save()

        return redirect('cadastro_poste:lista_De_Postes')
