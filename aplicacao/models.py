# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.exceptions import ValidationError
from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db.models import Sum


class Clientes(models.Model):
    nome = models.CharField(max_length=50)
    telefone = models.CharField(max_length=15, null=True, blank=True)
    celular = models.CharField(max_length=15, null=True, blank=True)
    nascimento = models.DateField(null=True, blank=True)
    email = models.CharField(max_length=25, null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True, blank=True)
    atualizado_em = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ("nome",)


class Profissionais(models.Model):
    nome = models.CharField(max_length=50)
    telefone = models.CharField(max_length=15, null=True, blank=True)
    celular = models.CharField(max_length=15, null=True, blank=True)
    nascimento = models.DateField(null=True, blank=True)
    email = models.CharField(max_length=25, null=True, blank=True)
    comissao = models.DecimalField(max_digits=10, decimal_places=2)
    criado_em = models.DateTimeField(auto_now_add=True, blank=True)
    atualizado_em = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Profissional"
        verbose_name_plural = "Profissionais"
        ordering = ("nome",)


class Especializacao(models.Model):
    nome = models.CharField(max_length=50)
    profissional = models.ForeignKey(Profissionais, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Especialização"
        verbose_name_plural = "Especializações"
        ordering = ("nome",)


class Servicos(models.Model):
    nome = models.CharField(max_length=50)
    duracao = models.IntegerField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    profissional = models.ForeignKey(Profissionais, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Serviço"
        verbose_name_plural = "Serviços"
        ordering = ["nome"]


class AgendaServico(models.Model):
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    profissional = models.ForeignKey(Profissionais, on_delete=models.CASCADE)
    servico = models.ManyToManyField(Servicos)
    data = models.DateField()
    hora = models.TimeField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    observacao = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.cliente.nome

    class Meta:
        verbose_name = "Agenda de Serviço"
        verbose_name_plural = "Agenda de Serviços"

    def check_overlap(self, fixed_start, fixed_end, new_start, new_end):
        overlap = False
        if new_start == fixed_end or new_end == fixed_start:  # edge case
            overlap = False
        elif (new_start >= fixed_start and new_start <= fixed_end) or (
            new_end >= fixed_start and new_end <= fixed_end
        ):  # innner limits
            overlap = True
        elif new_start <= fixed_start and new_end >= fixed_end:  # outter limits
            overlap = True

        return overlap

    def get_absolute_url(self):
        url = reverse(
            "admin:%s_%s_change" % (self._meta.app_label, self._meta.model_name),
            args=[self.id],
        )
        return '<a href="%s">%s</a>' % (url, str(self.cliente))

    def save(self, *args, **kwargs):
        profissional = Profissionais.objects.get(pk=self.profissional.id)
        pagamento = None
        try:
            pagamento = Pagamento.objects.get(agenda__id=self.pk)
        except:
            pass
        if pagamento:
            if profissional.comissao == 0:
                Comissoes.objects.filter(caixa=pagamento.caixa, agenda=self.pk).delete()
                pagamento.caixa.valor = pagamento.valor
                pagamento.caixa.save()
            else:
                comissao = Comissoes.objects.filter(
                    caixa=pagamento.caixa, agenda=self.pk
                )
                if not (comissao):
                    Comissoes.objects.create(
                        profissional=profissional,
                        valor=(pagamento.valor / 100) * profissional.comissao,
                        data=self.data,
                        caixa=pagamento.caixa,
                        agenda=self,
                    )

        super().save(*args, **kwargs)


TIPO_MOEDA = (
    ("DINHEIRO", "Dinheiro"),
    ("PIX", "Pix"),
    ("CARTÂO_DEBITO", "Cartão Débito"),
    ("CARTÂO_CREDITO", "Cartão Crédito"),
    ("CHEQUE", "Cheque"),
)


class Caixa(models.Model):
    data = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.data.strftime("%d-%m-%Y"))

    def save(self, *args, **kwargs):
        pagamentos = Pagamento.objects.filter(caixa=self.pk).values("valor")
        self.valor = pagamentos.aggregate(Sum("valor")).get("valor__sum") or 0
        pagamentos = Pagamento.objects.filter(caixa=self.pk)
        comissoes = Comissoes.objects.filter(caixa=self.pk).values("valor")
        total_comissao = comissoes.aggregate(Sum("valor")).get("valor__sum") or 0
        self.valor = self.valor - total_comissao
        super().save(*args, **kwargs)


class Pagamento(models.Model):

    valor = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_moeda = models.CharField(
        max_length=30, choices=TIPO_MOEDA, default="DINHEIRO", null=True, blank=True
    )
    data = models.DateTimeField(auto_now=True, blank=True)
    agenda = models.ForeignKey(AgendaServico, on_delete=models.CASCADE)
    caixa = models.ForeignKey(Caixa, on_delete=models.CASCADE, null=True, blank=True)
    efetuado = models.BooleanField(default=False)

    def __str__(self):
        val = str(self.agenda)
        return str(self.valor) + " " + val

    def clean(self):
        if not self.caixa:
            raise ValidationError("Voce precisa escolher um CAIXA")
        if not (self.tipo_moeda):
            raise ValidationError("Voce precisa escolher TIPO de MOEDA ")

    def save(self, *args, **kwargs):
        if not (self.tipo_moeda):
            self.clean()

        if not self.efetuado:
            taxa = self.agenda.profissional.comissao
            profissional = self.agenda.profissional
            agenda = AgendaServico.objects.get(self.agenda.pk)
            if self.agenda.profissional.comissao > 0:
                Comissoes.objects.create(
                    profissional=profissional,
                    valor=(self.valor / 100) * taxa,
                    data=self.data,
                    caixa=self.caixa,
                    agenda=agenda
                )
            self.efetuado = True
        super().save(*args, **kwargs)

    def delete(self):
        self.caixa
        self.caixa.valor = self.caixa.valor - self.valor
        self.caixa.save()
        super(Pagamento, self).delete()


class Produto(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.CharField(max_length=255, null=True, blank=True)
    valor_custo = models.DecimalField(max_digits=10, decimal_places=2)
    valor_venda = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.IntegerField()

    def __str__(self):
        return self.nome


class Pedido(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    valor_venda = models.DecimalField(max_digits=10, decimal_places=2)
    agenda = models.ForeignKey(
        AgendaServico, on_delete=models.CASCADE, null=True, blank=True
    )


class Comissoes(models.Model):
    profissional = models.ForeignKey(Profissionais, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateTimeField(auto_now=True, blank=True)
    caixa = models.ForeignKey(Caixa, on_delete=models.SET_NULL, null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True, blank=True)
    atualizado_em = models.DateTimeField(auto_now=True, blank=True)
    agenda = models.ForeignKey(
        AgendaServico, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.profissional.nome

    class Meta:
        verbose_name = "Comissão"
        verbose_name_plural = "Comissões"
        ordering = ["profissional"]
