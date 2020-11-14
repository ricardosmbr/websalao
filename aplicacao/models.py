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


class Event(models.Model):
    day = models.DateField('Dias do evento', help_text='Dias do evento')
    start_time = models.TimeField('Hora inicial', help_text='Hora inicial')
    end_time = models.TimeField('Hora final', help_text=u'Hora final')
    notes = models.TextField('Anotações', help_text='TAnotações', blank=True, null=True)

    class Meta:
        verbose_name = 'Agenda'
        verbose_name_plural = 'Agenda'

    def check_overlap(self, fixed_start, fixed_end, new_start, new_end):
        overlap = False
        if new_start == fixed_end or new_end == fixed_start:  # edge case
            overlap = False
        elif (new_start >= fixed_start and new_start <= fixed_end) or (new_end >= fixed_start and new_end <= fixed_end):  # innner limits
            overlap = True
        elif new_start <= fixed_start and new_end >= fixed_end:  # outter limits
            overlap = True
        print(overlap)
        return overlap

    def get_absolute_url(self):
        url = reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[self.id])
        return u'<a href="%s">%s</a>' % (url, str(self.start_time))

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError('Hora final deve ser após a hora inicial')

        events = Event.objects.filter(day=self.day)
        if events.exists():
            for event in events:
                print(event.start_time, event.end_time)
                if self.check_overlap(event.start_time, event.end_time, self.start_time, self.end_time):
                    raise ValidationError(
                        'Há uma sobreposição com outro evento: ' + str(event.day) + ', ' + str(
                            event.start_time) + '-' + str(event.end_time))
