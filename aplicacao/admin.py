from django.contrib import admin
from .models import Clientes, Profissionais, Especializacao, Servicos

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


admin.site.register(Clientes, ClientesAdmin)
admin.site.register(Profissionais, ProfissionaisAdmin)
