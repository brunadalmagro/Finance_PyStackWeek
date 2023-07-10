from django.shortcuts import render, redirect, get_object_or_404
from perfil.models import Categoria, Conta
from .models import Valores
from django.http import HttpResponse, FileResponse
from django.contrib.messages import constants
from django.contrib import messages
from datetime import datetime
from django.template.loader import render_to_string
import os
from django.conf import settings
from weasyprint import HTML
from io import BytesIO


def novo_valor(request):
    if request.method == 'GET':
        contas = Conta.objects.all()
        categorias = Categoria.objects.all()
        return render(request, 'novo_valor.html', {"contas": contas, "categorias": categorias})

    elif request.method == 'POST':
        valor = request.POST.get('valor')
        categoria = request.POST.get('categoria')
        descricao = request.POST.get('descricao')
        data = request.POST.get('data')
        conta = request.POST.get('conta')
        tipo = request.POST.get('tipo')

        if not valor or not categoria or not data or not conta or not tipo:
            messages.error(request, 'Preencha todos os campos obrigatórios.')
            return redirect('/extrato/novo_valor')

        try:
            valor = float(valor)
        except ValueError:
            messages.error(request, 'O valor deve ser um número válido.')
            return redirect('/extrato/novo_valor')

        try:
            conta_obj = get_object_or_404(Conta, id=conta)
        except:
            messages.error(request, 'A conta selecionada não existe.')
            return redirect('/extrato/novo_valor')

        valores = Valores(
            valor=valor,
            categoria_id=categoria,
            descricao=descricao,
            data=data,
            conta_id=conta,
            tipo=tipo,
        )

        valores.save()

        if tipo == 'E':
            conta_obj.valor += valor
        else:
            conta_obj.valor -= valor

        conta_obj.save()

        if tipo == 'E':
            messages.success(request, 'Entrada cadastrada com sucesso.')
        elif tipo == 'S':
            messages.success(request, 'Saída cadastrada com sucesso.')
        else:
            messages.success(request, 'Cadastro realizado com sucesso.')

        return redirect('/extrato/novo_valor')


def view_extrato(request):
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()

    conta_get = request.GET.get('conta')
    categoria_get = request.GET.get('categoria')
    valores = Valores.objects.filter(data__month=datetime.now().month)

    if conta_get:
        valores = valores.filter(conta__id=conta_get)

    if categoria_get:
        valores = valores.filter(categoria__id=categoria_get)

    # Verifica se o parâmetro 'categoria' está definido para mostrar ou ocultar o botão de limpar filtros
    categoria_filtrada = categoria_get is not None

    # Verifica se o parâmetro 'conta' está definido para mostrar ou ocultar o botão de limpar filtros
    conta_filtrada = conta_get is not None

    return render(request, 'view_extrato.html', {
        'valores': valores,
        'contas': contas,
        'categorias': categorias,
        'categoria_filtrada': categoria_filtrada,
        'conta_filtrada': conta_filtrada,
    })


def exportar_pdf(request):
    valores = Valores.objects.filter(data__month=datetime.now().month)

    path_template = os.path.join(settings.BASE_DIR, 'templates/partials/extrato.html')
    template_render = render_to_string(path_template, {'valores': valores})

    path_output = BytesIO()

    HTML(string=template_render).write_pdf(path_output)

    path_output.seek(0)

    return FileResponse(path_output, filename='extrato.pdf')
