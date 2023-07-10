from django.db import models
from datetime import datetime
from django.db.models import Sum

class Categoria(models.Model):
    categoria = models.CharField(max_length=50)
    essencial = models.BooleanField(default=False)
    valor_planejamento = models.FloatField(default=0)


    def __str__(self):
        return self.categoria
    
    def total_gasto(self):
        from extrato.models import Valores
        valores = Valores.objects.filter(categoria__id=self.id).filter(data__month=datetime.now().month).aggregate(Sum('valor'))
        return valores['valor__sum'] if valores['valor__sum'] else 0
    
    def calcula_percentual_gasto_por_categoria(self):
        if self.valor_planejamento == 0:
            return 0
        
        return int((self.total_gasto() / self.valor_planejamento) * 100)

    def calcula_percentual_gasto_total(self):
        categorias = Categoria.objects.all()
        total_planejado = categorias.aggregate(Sum('valor_planejamento'))['valor_planejamento__sum']
        total_gasto = categorias.aggregate(Sum('total_gasto'))['total_gasto__sum']

        if total_planejado is None:
            total_planejado = 0
        if total_gasto is None:
            total_gasto = 0

        if total_planejado == 0:
            return 0

        return int((total_gasto / total_planejado) * 100)


class Conta(models.Model):
    banco_choices = (
        ('Nu', 'Nubank'),
        ('CE', 'Caixa Econômica'),
        ('C6', 'C6 Bank'),
        ('Inter', 'Inter'),
        ('BR', 'Bradesco'),
        ('Santander', 'Santander'),
        ('Itaú', 'Itaú'),
        ('BB', 'Banco do Brasil'),
        ('Will', 'Will Bank'),
    )
    
    tipo_choices = (
        ('PF', 'Pessoa física'),
        ('PJ', 'Pessoa Jurídica'),
    )
    
    apelido = models.CharField(max_length=50)
    banco = models.CharField(max_length=20, choices=banco_choices)
    tipo = models.CharField(max_length=2, choices=tipo_choices)
    valor = models.FloatField()
    icone = models.ImageField(upload_to="icones")
    
    def __str__(self):
        return self.apelido

class Despesa(models.Model):
    nome = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    # Outros campos da despesa

    def __str__(self):
        return self.nome