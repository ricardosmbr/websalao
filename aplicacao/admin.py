from django.contrib import admin
from .models import (
    Clientes, 
    Profissionais, 
    Especializacao, 
    Servicos,
    AgendaServico
)
from .utils import AgendaEvent
from django.urls import reverse
import datetime
import calendar
from calendar import HTMLCalendar
from django.utils.safestring import mark_safe

class ClientesAdmin(admin.ModelAdmin):

    fields = (
        "nome",
        "telefone",
        "celular",
        "nascimento",
        "email",
    )
    readonly_fields = ('criado_em', 'atualizado_em',)
    list_display = ("nome", "email", "criado_em", "atualizado_em")
    model = Clientes


class EspecializacaoInline(admin.TabularInline):
    model = Especializacao


class ServicosInline(admin.TabularInline):
    model = Servicos

class ProfissionaisAdmin(admin.ModelAdmin):

    fields = (
        "nome",
        "telefone",
        "celular",
        "nascimento",
        "email",
        "comissao",
    )
    list_display = ("nome", "email", "comissao")
    inlines = [
        EspecializacaoInline,
        ServicosInline,
    ]
    model = Profissionais

class AgendaServicoAdmin(admin.ModelAdmin):

    list_display = ['cliente', 'data', 'hora', 'valor', 'observacao']
    change_list_template = 'admin/events/agenda.html'
    # model = AgendaServico
    def changelist_view(self, request, extra_context=None):
        after_day = request.GET.get('day__gte', None)
        extra_context = extra_context or {}
        
        if not after_day:
            d = datetime.date.today()
        else:
            try:
                split_after_day = after_day.split('-')
                d = datetime.date(year=int(split_after_day[0]), month=int(split_after_day[1]), day=1)
            except:
                d = datetime.date.today()

        previous_month = d-datetime.timedelta(days=7)
        next_month = d+datetime.timedelta(days=7)  # find last day of current month
        extra_context['previous_month'] = reverse('admin:events_event_changelist') + '?day__gte=' + str(
            previous_month)
        extra_context['next_month'] = reverse('admin:events_event_changelist') + '?day__gte=' + str(next_month)

        cal = AgendaEvent()
        html_calendar = cal.formatmonth(d.year, d.month, withyear=True)
        html_calendar = html_calendar.replace('<td ', '<td  width="150" height="150"')
        extra_context['agenda'] = mark_safe(html_calendar)
        # print(extra_context)
        return super(AgendaServicoAdmin, self).changelist_view(request, extra_context)




admin.site.register(Clientes, ClientesAdmin)
admin.site.register(Profissionais, ProfissionaisAdmin)
admin.site.register(AgendaServico, AgendaServicoAdmin)