from pyexpat import model
import graphene
from graphene_django import DjangoObjectType
from .models import (
    Clientes,
    AgendaServico,
    Caixa,
    Profissionais,
    Produto,
    Pagamento,
    Comissoes
)
 

class AgendaServicoType(DjangoObjectType):

    class Meta:
        model=AgendaServico

 
class ClientesType(DjangoObjectType):

    class Meta:
        model=Clientes


class CaixaType(DjangoObjectType):

    class Meta:
        model=Caixa


class ProfissionaisType(DjangoObjectType):

    class Meta:
        model=Profissionais


class ProdutoType(DjangoObjectType):

    class Meta:
        model=Produto


class PagamentoType(DjangoObjectType):

    class Meta:
        model=Pagamento


class ComissoesType(DjangoObjectType):

    class Meta:
        model=Comissoes


class Query(graphene.ObjectType):

    clientes = graphene.List(ClientesType)
    agendas = graphene.List(AgendaServicoType)
    caixas = graphene.List(CaixaType)
    proficionais = graphene.List(ProfissionaisType)
    produto = graphene.List(ProdutoType)
    pagamento = graphene.List(PagamentoType)
    comissoes = graphene.List(ComissoesType)

    def resolve_clientes(root,info):
        return Clientes.objects.all()

    def resolve_agendas(root,info):
        return AgendaServico.objects.all()

    def resolve_acaixas(root,info):
        return Caixa.objects.all()

    def resolve_proficionais(root,info):
        return Profissionais.objects.all()

    def resolve_produto(root,info):
        return Produto.objects.all()

    def resolve_pagamento(root,info):
        return Pagamento.objects.all()

    def resolve_comissoes(root,info):
        return Comissoes.objects.all()

schema = graphene.Schema(query=Query)