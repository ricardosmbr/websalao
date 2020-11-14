from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse

DIAS_SEMANA = (
    ("SEGUNDA", "Segunda-feira"),
    ("TERÇA", "Terça_feira"),
    ("QUARTA", "Quarta-feira"),
    ("QUINTA", "Quinta-feira"),
    ("SEXTA", "Sexta-feira"),
    ("SABADO", "Sábado"),
    ("Domingo", "Domingo"),
)


class Configuracao(models.Model):
    nome = models.CharField(max_length=50)
    endereco = models.CharField(max_length=50)
    cep = models.CharField(max_length=15)
    telefone = models.CharField(max_length=15)

    def __str__(self):
        return self.nome


class Dias_semana(models.Model):
    nome = models.CharField(max_length=50, choices=DIAS_SEMANA)
    hora_inicio = models.TimeField(blank=True, null=True)
    hora_fim = models.TimeField(blank=True, null=True)
    id_configuracao = models.ForeignKey(Configuracao, on_delete=models.CASCADE)
