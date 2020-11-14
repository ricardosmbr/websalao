from django.db import models
from __future__ import unicode_literals


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


class Event(models.Model):
    day = models.DateField(u'Day of the event', help_text=u'Day of the event')
    start_time = models.TimeField(u'Starting time', help_text=u'Starting time')
    end_time = models.TimeField(u'Final time', help_text=u'Final time')
    notes = models.TextField(u'Textual Notes', help_text=u'Textual Notes', blank=True, null=True)

    class Meta:
        verbose_name = u'Scheduling'
        verbose_name_plural = u'Scheduling'
