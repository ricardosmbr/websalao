from calendar import HTMLCalendar
from datetime import datetime as dtime, date, time
from datetime import timedelta
from .models import AgendaServico, Comissoes, Profissionais, Caixa, Pagamento
from configuracao.models import Configuracao, Dias_semana
from django.db.models.signals import post_save
from django.dispatch import receiver

# from .models import Event


class AgendaEvent(HTMLCalendar):
    def __init__(self, events=None):
        super(AgendaEvent, self).__init__()
        self.events = events

    def formatday(self, day, hora, pro, events):
        """
        Return a day as a table cell.
        """
        # print(dir(hora))
        # print(hora.seconds/3600)
        if hora:
            events_from_day = events.filter(
                data__day=day, hora__hour=int(hora.seconds / 3600), profissional=pro
            )
            # print(events_from_day)
            events_html = "<ul>"
            for event in events_from_day:
                # print(event.hora, hora)
                events_html += event.get_absolute_url() + "<br>"
            events_html += "</ul>"
        else:
            return ""

        if day == 0:
            return '<td class="noday">&nbsp;</td>'  # day outside month
        else:
            return '<td class="">%s</td>' % (events_html)

    def formatweek(self, theweek, events):
        """
        Return a complete week as a table row.
        """
        s = "".join(self.formatday(d, wd, events) for (d, wd) in theweek)

        return "<tr>%s</tr>" % s

    def formatmonth(self, data, theyear, themonth, withyear=True):
        """
        Return a formatted month as a table.
        """
        events = AgendaServico.objects.filter(data__month=themonth,data__year=theyear)
        proficionais = Profissionais.objects.all().order_by("nome")
        confi = Configuracao.objects.all().first()
        hora = Dias_semana.objects.filter(id_configuracao=confi)
        today = data
        dias = (
            "Segunda-feira",
            "Terça-feira",
            "Quarta-feira",
            "Quinta-feira",
            "Sexta-feira",
            "Sábado",
            "Domingo",
        )
        meses = (
            "Janeiro",
            "Fevereiro",
            "Março",
            "Abril",
            "Maio",
            "Junho",
            "Julho",
            "Agosto",
            "Setembro",
            "Outubro",
            "Nvembro",
            "Dezembro",
        )
        v = []
        a = v.append
        a("<div>")
        a(
            (
                dias[today.weekday()]
                + " "
                + str(today.day)
                + " de "
                + meses[today.month - 1]
                + " de "
                + str(today.year)
            )
        )
        a("</div>")
        a('<table border="0" cellpadding="0" cellspacing="0" class="month">')
        profi = "<tr><th>Horário</th>"
        for pro in proficionais:
            profi = profi + "<th>" + pro.nome + "</th>"
        profi = profi + "</tr>"
        a("\n")
        a(profi)
        linha = "<tr>"
        qtde = 0
        hora_ini = 0
        for coluna in hora:
            # print(coluna.hora_inicio,coluna.hora_fim)
            if today.weekday() == 0 and coluna.nome == "SEGUNDA":
                qtde = coluna.hora_fim.hour - coluna.hora_inicio.hour
                hora_ini = coluna.hora_inicio.hour
            elif today.weekday() == 1 and coluna.nome == "TERÇA":
                qtde = coluna.hora_fim.hour - coluna.hora_inicio.hour
                hora_ini = coluna.hora_inicio.hour
            elif today.weekday() == 2 and coluna.nome == "QUARTA":
                qtde = coluna.hora_fim.hour - coluna.hora_inicio.hour
                hora_ini = coluna.hora_inicio.hour
            elif today.weekday() == 3 and coluna.nome == "QUINTA":
                qtde = coluna.hora_fim.hour - coluna.hora_inicio.hour
                hora_ini = coluna.hora_inicio.hour
            elif today.weekday() == 4 and coluna.nome == "SEXTA":
                qtde = coluna.hora_fim.hour - coluna.hora_inicio.hour
                hora_ini = coluna.hora_inicio.hour
            elif today.weekday() == 5 and coluna.nome == "SABADO":
                qtde = coluna.hora_fim.hour - coluna.hora_inicio.hour
                hora_ini = coluna.hora_inicio.hour
            elif today.weekday() == 6 and coluna.nome == "Domingo":
                qtde = coluna.hora_fim.hour - coluna.hora_inicio.hour
                hora_ini = coluna.hora_inicio.hour
        # print(qtde)
        for i in range(qtde + 1):
            uma = timedelta(hours=hora_ini + i)
            linha = linha + "<th>" + str(uma) + "</th>"
            for pro in proficionais:
                # linha = linha + '<th></th>'
                linha = linha + self.formatday(today.day, uma, pro, events)
                # print(linha)
            linha = linha + "</tr>"
            a(linha + "\n")
            linha = ""

        a("\n")
        a("</table>")
        a("\n")
        # print(''.join(v))
        return "".join(v)
        return None


@receiver(post_save, sender=Pagamento)
def salva_caixa(sender, instance, **kwargs):
    caixa = Caixa.objects.get(id=instance.caixa.id)
    comissao = Comissoes.objects.filter(caixa=caixa, agenda=instance.agenda.id)
    for com in comissao:
        if instance.agenda.profissional.comissao > 0:
            com.valor = (instance.valor / 100) * instance.agenda.profissional.comissao
            com.save()
    caixa.save()
