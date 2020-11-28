from calendar import HTMLCalendar
from datetime import datetime as dtime, date, time
from datetime import timedelta
from .models import AgendaServico, Profissionais
from configuracao.models import Configuracao, Dias_semana
# from .models import Event


class AgendaEvent(HTMLCalendar):
    def __init__(self, events=None):
        super(AgendaEvent, self).__init__()
        self.events = events
    def formatday(self, day, weekday, events):
        """
        Return a day as a table cell.
        """
        events_from_day = events.filter(day__day=day)
        events_html = "<ul>"
        for event in events_from_day:
            events_html += event.get_absolute_url() + "<br>"
        events_html += "</ul>"

        if day == 0:
            return '<td class="noday">&nbsp;</td>'  # day outside month
        else:
            return '<td class="%s">%d%s</td>' % (self.cssclasses[weekday], day, events_html)

    def formatweek(self, theweek, events):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd, events) for (d, wd) in theweek)

        return '<tr>%s</tr>' % s

    def formatmonth(self, theyear, themonth, withyear=True):
        """
        Return a formatted month as a table.
        """
        # print(themonth)
        events = AgendaServico.objects.filter(data__month=themonth)
        proficionais = Profissionais.objects.all()
        confi = Configuracao.objects.all().first()
        hora  = Dias_semana.objects.filter(id_configuracao=confi)
        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="month">')
        profi = '<tr><th>Horário</th>'
        for pro in proficionais:
            profi = profi + '<th>' + pro.nome+'</th>'
        profi = profi+'</tr>'
        a('\n')
        a(profi)
        linha = '<tr>'
        qtde = 0
        today = date.today()
        for coluna in hora:
            if(today.weekday()==0 and coluna.nome =='SEGUNDA'):
                qtde = (coluna.hora_fim.hour - coluna.hora_inicio.hour)
            elif(today.weekday()==1 and coluna.nome =='TERÇA'):
                qtde = (coluna.hora_fim.hour - coluna.hora_inicio.hour)
            elif(today.weekday()==2 and coluna.nome =='QUARTA'):
                qtde = (coluna.hora_fim.hour - coluna.hora_inicio.hour)
            elif(today.weekday()==3 and coluna.nome =='QUINTA'):
                qtde = (coluna.hora_fim.hour - coluna.hora_inicio.hour)
            elif(today.weekday()==4 and coluna.nome =='SEXTA'):
                qtde = (coluna.hora_fim.hour - coluna.hora_inicio.hour)
            elif(today.weekday()==5 and coluna.nome =='SABADO'):
                qtde = (coluna.hora_fim.hour - coluna.hora_inicio.hour)
            elif(today.weekday()==6 and coluna.nome =='Domingo'):
                qtde = (coluna.hora_fim.hour - coluna.hora_inicio.hour)

        for i in range(qtde):
            uma = timedelta(hours=qtde + i)
            linha = linha + '<th>'+str(uma)+'</th>'
            for pro in proficionais:
                linha = linha + '<th></th>'
            linha = linha + '</tr>'
            a(linha + '\n')
            linha = ''
            meia = timedelta(hours=qtde + i)+timedelta(minutes=30)
            linha = linha + '<th>'+str(meia)+'</th>'
            for pro in proficionais:
                linha = linha + '<th></th>'
            linha = linha + '</tr>'
            a(linha + '\n')
            linha = ''
        # print("passo 1")
        # a(self.formatmonthname(theyear, themonth, withyear=withyear)) 
        # print(''.join(v))       
        a('\n')
        # a(self.formatweekheader())
        a('\n')
        # for week in self.monthdays2calendar(theyear, themonth):
        #     # a(self.formatweek(week, events))
        #     a('\n')
        a('</table>')
        # a('\n')
        # print(''.join(v))
        return ''.join(v)
        return None