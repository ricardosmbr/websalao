from django.db import models


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


class Especializacao(models.Model):
    nome = models.CharField(max_length=50)
    profissional = models.ForeignKey(Profissionais, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Especialização"
        verbose_name_plural = "Especializações"


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
