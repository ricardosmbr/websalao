from django.contrib import admin
from .models import Configuracao, Dias_semana


class Dias_semanaInline(admin.TabularInline):
    model = Dias_semana


class ConfiguracaoAdmin(admin.ModelAdmin):

    fields = (
        "nome",
        "endereco",
        "cep",
        "telefone",
    )
    list_display = ("nome", "endereco", "cep", "telefone")
    inlines = [
        Dias_semanaInline,
    ]
    model = Configuracao


admin.site.register(Configuracao, ConfiguracaoAdmin)
