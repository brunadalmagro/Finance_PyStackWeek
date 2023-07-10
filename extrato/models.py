from django.db import models

class Valores(models.Model):
    choice_tipo = (
        ('E', 'Entrada'),
        ('S', 'Saída')
    )
    
    valor = models.FloatField()
    categoria = models.ForeignKey('perfil.Categoria', on_delete=models.DO_NOTHING)
    descricao = models.TextField()
    data = models.DateField()
    conta = models.ForeignKey('perfil.Conta', on_delete=models.DO_NOTHING)
    tipo = models.CharField(max_length=1, choices=choice_tipo)

    def __str__(self):
        return self.descricao
