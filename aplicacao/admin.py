from django.contrib import admin
from django.db import models
from .models import (
    Clientes,
    Profissionais,
    Especializacao,
    Servicos,
    AgendaServico,
    Pagamento,
    Caixa,
    Produto,
    Pedido,
    Comissoes,
)
from .utils import AgendaEvent
from django.urls import reverse
import datetime
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from django.http import HttpResponse
import csv


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


class ClientesAdmin(admin.ModelAdmin, ExportCsvMixin):

    fields = (
        "nome",
        "telefone",
        "celular",
        "nascimento",
        "email",
    )
    readonly_fields = (
        "criado_em",
        "atualizado_em",
    )
    list_display = ("nome", "telefone", "celular", "nascimento")
    model = Clientes
    actions = ["export_as_csv"]


class EspecializacaoInline(admin.TabularInline):
    model = Especializacao


class ServicosAdmin(admin.ModelAdmin, ExportCsvMixin):
    model = Servicos


class ComissoesInline(admin.TabularInline):

    model = Comissoes
    readonly_fields = (
        "valor",
        "profissional",
        "agenda",
    )
    extra = 0


class PagamentoInline(admin.TabularInline):
    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(PagamentoInline, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == "caixa":
            field.queryset = Caixa.objects.all().order_by("data")
        return field

    model = Pagamento
    exclude = ("efetuado",)
    extra = 0


class ProdutoInline(admin.TabularInline):
    model = Produto
    exclude = ("valor_custo",)
    extra = 0


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("nome", "valor_venda")
    model = Produto


class PedidoInline(admin.TabularInline):
    list_display = ("produto", "quantidade", "valor_venda")
    model = Pedido
    extra = 0


class ProfissionaisAdmin(admin.ModelAdmin):

    fields = (
        "nome",
        "telefone",
        "celular",
        "nascimento",
        "email",
        "comissao",
    )
    list_display = ("nome", "telefone", "comissao")
    inlines = [
        EspecializacaoInline,
    ]
    model = Profissionais


class AgendaServicoAdmin(admin.ModelAdmin):

    list_display = ["cliente", "data", "hora", "valor", "observacao"]
    change_list_template = "admin/events/agenda.html"
    inlines = [PedidoInline, PagamentoInline]

    # model = AgendaServico
    def changelist_view(self, request, extra_context=None):
        after_day = request.GET.get("data__gte", None)
        # print(admin.site.urls)
        extra_context = extra_context or {}
        profi = Profissionais.objects.all().count()
        if profi:
            tamanho = '<td  width="' + str(900 / profi) + '" height="100"'
        else:
            tamanho = ""

        if not after_day:
            d = datetime.date.today()
        else:
            try:
                split_after_day = after_day.split("-")
                d = datetime.date(
                    year=int(split_after_day[0]),
                    month=int(split_after_day[1]),
                    day=int(split_after_day[2]),
                )
            except:
                d = datetime.date.today()

        previous_month = d - datetime.timedelta(days=1)
        next_month = d + datetime.timedelta(days=1)  # find last day of current month
        extra_context["previous_day"] = (
            reverse("admin:aplicacao_agendaservico_changelist")
            + "?data__gte="
            + str(previous_month)
        )
        extra_context["next_day"] = (
            reverse("admin:aplicacao_agendaservico_changelist")
            + "?data__gte="
            + str(next_month)
        )

        cal = AgendaEvent()
        html_calendar = cal.formatmonth(d, d.year, d.month, withyear=True)
        html_calendar = html_calendar.replace("<td ", tamanho)
        extra_context["agenda"] = mark_safe(html_calendar)
        # print(extra_context)
        return super(AgendaServicoAdmin, self).changelist_view(request, extra_context)


class CaixaAdmin(ImportExportModelAdmin, ExportCsvMixin):
    list_display = ["data", "valor"]
    model = Caixa
    inlines = [PagamentoInline, ComissoesInline]
    actions = ["export_as_csv"]

class ComissoesAdmin(admin.ModelAdmin):
    list_display = ["profissional","agenda", "data", "valor"]
    models = Comissoes
    ordering = ['-data']

admin.site.register(Clientes, ClientesAdmin)
admin.site.register(Servicos, ServicosAdmin)
admin.site.register(Profissionais, ProfissionaisAdmin)
admin.site.register(AgendaServico, AgendaServicoAdmin)
admin.site.register(Caixa, CaixaAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Comissoes, ComissoesAdmin)
