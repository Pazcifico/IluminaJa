from django.shortcuts import render, redirect, get_object_or_404
from .models import Lampada, Poste
from django.http import JsonResponse
import json


def lista_lampadas(request):
    lampadas = Lampada.objects.select_related('poste').all()
    return render(request, 'lampadas/lampada_list.html', {'lampadas': lampadas})


def adicionar_lampada(request):
    postes_disponiveis = Poste.objects.exclude(
        id__in=Lampada.objects.values_list('poste_id', flat=True))
    if request.method == 'POST':
        poste_id = request.POST.get('poste')
        tipo = request.POST.get('tipo')
        vida_util = int(request.POST.get('vida_util_meses'))
        data_instalacao = request.POST.get('data_instalacao')
        status = request.POST.get('status')

        poste = get_object_or_404(Poste, id=poste_id)
        Lampada.objects.create(
            poste=poste,
            tipo=tipo,
            vida_util_meses=vida_util,
            data_instalacao=data_instalacao,
            status=status
        )
        return redirect('cadastro_poste:lista_lampadas')

    return render(request, 'lampadas/lampada_form.html', {
        'postes': postes_disponiveis,
        'TIPO_CHOICES': Lampada.TIPO_CHOICES,
        'STATUS_CHOICES': Lampada.STATUS_CHOICES,
        'lampada': None
    })


def editar_lampada(request, pk):
    lampada = get_object_or_404(Lampada, pk=pk)
    if request.method == 'POST':
        lampada.tipo = request.POST.get('tipo')
        lampada.vida_util_meses = int(request.POST.get('vida_util_meses'))
        lampada.data_instalacao = request.POST.get('data_instalacao')
        lampada.status = request.POST.get('status')
        lampada.save()
        return redirect('cadastro_poste:lista_lampadas')

    return render(request, 'lampadas/lampada_form.html', {
        'lampada': lampada,
        'TIPO_CHOICES': Lampada.TIPO_CHOICES,
        'STATUS_CHOICES': Lampada.STATUS_CHOICES,
    })


def excluir_lampada(request, pk):
    lampada = get_object_or_404(Lampada, pk=pk)
    if request.method == 'POST':
        lampada.delete()
        return redirect('cadastro_poste:lista_lampadas')

    return render(request, 'lampadas/lampada_delete.html', {'lampada': lampada})


def cadastro_poste(request):
    if request.method == 'POST':
        request.session['problema'] = request.POST.get('problema')
        request.session['informacao'] = request.POST.get('informacao')
        return redirect('cadastro_poste:endereco_poste')
    return render(request, 'cadastro_poste/formulario.html')


def endereco_poste(request):
    if request.method == 'POST':
        cep = request.POST.get('cep')
        rua = request.POST.get('rua')
        numero = request.POST.get('numero')
        bairro = request.POST.get('bairro')
        cidade = request.POST.get('cidade')
        estado = request.POST.get('estado')

        problema = request.session.get('problema')
        informacao = request.session.get('informacao')

        Poste.objects.create(
            problema=problema,
            informacao=informacao,
            cep=cep,
            rua=rua,
            numero=numero,
            bairro=bairro,
            cidade=cidade,
            estado=estado
        )

        request.session.pop('problema', None)
        request.session.pop('informacao', None)

        return redirect('cadastro_poste:sucesso')

    return render(request, 'cadastro_poste/endereco_poste.html')


def sucesso(request):
    return render(request, 'cadastro_poste/sucesso.html')


def lista_de_postes(request):
    postes = Poste.objects.all().order_by('-id')[:5]
    return render(request, 'cadastro_poste/lista_poste.html', {'postes': postes})


def mapa_view(request):
    postes = [
        {"lat": -14.223, "lng": -42.782, "titulo": "Poste 1"},
        {"lat": -14.225, "lng": -42.780, "titulo": "Poste 2"},
    ]
    dados_postes_json = json.dumps(postes)
    return render(request, "mapa_template.html", {"dados_postes_json": dados_postes_json})


def lampada_por_poste(request, poste_id):
    try:
        lampada = Lampada.objects.get(poste_id=poste_id)
        return JsonResponse({
            'id': lampada.id,
            'tipo': lampada.tipo,
            'potencia': lampada.potencia
        })
    except Lampada.DoesNotExist:
        return JsonResponse({})
