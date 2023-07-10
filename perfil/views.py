from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Conta, Categoria
from django.contrib import messages
from django.contrib.messages import constants
from .utils import calcula_total, calcula_equilibrio_financeiro
from extrato.models import Valores
from datetime import datetime, date
from django.db.models import Sum
from .models import Despesa

import re

def home(request):
    valores = Valores.objects.filter(data__month=datetime.now().month)
    entradas = valores.filter(tipo='E')
    saidas = valores.filter(tipo='S')

    total_entradas = calcula_total(entradas, 'valor')
    total_saidas = calcula_total(saidas, 'valor')
    
    saldo_mensal = total_entradas - total_saidas

    contas = Conta.objects.all()
    total_contas = calcula_total(contas, 'valor')

    percentual_gastos_essenciais, percentual_gastos_nao_essenciais = calcula_equilibrio_financeiro()

    despesa_mensal = calcula_total(saidas, 'valor')
    total_livre = saldo_mensal - despesa_mensal
    
    despesas = Despesa.objects.filter(data__year=2023, data__month=7)  # Filtra as despesas de julho de 2023, você pode modificar esse filtro de acordo com suas necessidades


    # Verificação do total livre - Nesse código, após calcular o valor da despesa mensal e do saldo mensal, são feitas verificações para garantir que os valores não sejam negativos. Caso sejam negativos, os valores são definidos como zero. Dessa forma se os resultados da soma forem positivos o resultado é igual a zero.
    ##   if total_livre < 0:
    ##    total_livre = 0
   
    
    return render(request, 'home.html', {"contas": contas, "total_contas": total_contas, 'total_entradas': total_entradas, 'total_saidas': total_saidas, 'percentual_gastos_essenciais': int(percentual_gastos_essenciais), 'percentual_gastos_nao_essenciais': int(percentual_gastos_nao_essenciais), 'saldo_mensal': saldo_mensal, 'despesa_mensal': despesa_mensal, 'total_livre': total_livre, "despesas": despesas,})





def gerenciar(request):
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()
    
    total_contas = calcula_total(contas, 'valor')
    
    return render(request, 'gerenciar.html', {'contas': contas, 'total_contas': total_contas, 'categorias': categorias})


def cadastrar_banco(request):
    bancos = Conta.banco_choices
    context = {'bancos': bancos}
        
    if request.method == 'POST':
        apelido = request.POST.get('apelido')
        banco = request.POST.get('banco')
        tipo = request.POST.get('tipo')
        valor = request.POST.get('valor')
        icone = request.FILES.get('icone')
        
        if len(apelido.strip()) == 0 or len(valor.strip()) == 0:
            messages.error(request, 'Preencha todos os campos')
            return redirect('/perfil/gerenciar/')

        # Validação do apelido
        if not re.match(r'^[a-zA-Z0-9\s]+$', apelido):
            messages.error(request, 'Apelido inválido. Utilize apenas letras, números e espaços')
            return redirect('/perfil/gerenciar/')

        # Validação do valor
        if not re.match(r'^\d+(\.\d{1,2})?$', valor):
            messages.error(request, 'Valor inválido. Insira um número válido')
            return redirect('/perfil/gerenciar/')

        conta = Conta(
            apelido=apelido,
            banco=banco,
            tipo=tipo,
            valor=valor,
            icone=icone
        )

        conta.save()

        messages.success(request, 'Conta cadastrada com sucesso!')
    
    return redirect('/perfil/gerenciar/')


def deletar_banco(request, id):
    conta = Conta.objects.get(id=id)
    conta.delete()
    messages.success(request, 'Conta excluída com sucesso!')
    return redirect('/perfil/gerenciar/')


def cadastrar_categoria(request):
    nome = request.POST.get('categoria')
    essencial = request.POST.get('essencial')

    if essencial == 'on':
        essencial = True
    else:
        essencial = False

    if not nome:
        messages.error(request, 'Preencha o campo obrigatório: Nome da categoria')
        return redirect('/perfil/gerenciar/')

    # Validação do nome da categoria
    if not re.match(r'^[a-zA-Z0-9\sÀ-ÿ]+$', nome):
        messages.error(request, 'Nome da categoria inválido. Utilize apenas letras, números, espaços e caracteres acentuados')
        return redirect('/perfil/gerenciar/')

    categoria = Categoria(
        categoria=nome,
        essencial=essencial
    )

    categoria.save()

    messages.add_message(request, constants.SUCCESS, 'Categoria cadastrada com sucesso')
    return redirect('/perfil/gerenciar/')




def update_categoria(request, id):
    categoria = Categoria.objects.get(id=id)
    categoria.essencial = not categoria.essencial
    categoria.save()
    
    return redirect('/perfil/gerenciar/')
    
def dashboard(request):
    dados = {}
    categorias = Categoria.objects.all()

    for categoria in categorias:
        dados[categoria.categoria] = Valores.objects.filter(categoria=categoria).aggregate(Sum('valor'))['valor__sum']

    return render(request, 'dashboard.html', {'labels': list(dados.keys()), 'values': list(dados.values())})