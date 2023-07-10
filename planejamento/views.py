from django.shortcuts import render, redirect
from perfil.models import Categoria
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.messages import constants
import json
import re

def definir_planejamento(request):
    categorias = Categoria.objects.all()

    if request.method == 'POST':
        valor = request.POST.get('valor')

        # Validação e conversão do valor para float
        try:
            valor_float = float(re.sub(r'[^\d.]', '', valor))
        except ValueError:
            messages.error(request, 'Valor inválido. Insira um número válido')
            return redirect('/definir_planejamento/')
        
        # Cadastro realizado com sucesso
        messages.success(request, 'Cadastro realizado com sucesso')

    return render(request, 'definir_planejamento.html', {'categorias': categorias})

@csrf_exempt
def update_valor_categoria(request, id):
    novo_valor = json.load(request)['novo_valor']
    categoria = Categoria.objects.get(id=id)
    categoria.valor_planejamento = novo_valor
    categoria.save()

    # Redireciona o usuário para a página desejada após o cadastro
    return redirect('/definir_planejamento/')


def ver_planejamento(request):
    categorias = Categoria.objects.all()
    return render(request, 'ver_planejamento.html', {'categorias': categorias})
