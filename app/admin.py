from django.contrib import admin

from .models import (
    AnaliseContrato,
    Contrato,
    Empresa,
    Estagio,
    Instituicao,
    ParecerInstitucional,
    Pendencia,
    RegraValidacao,
    RelatorioConformidade,
    SistemaValidador,
    Usuario,
)


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cpf', 'email']
    search_fields = ['nome', 'cpf', 'email']


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['razao_social', 'cnpj', 'responsavel']
    search_fields = ['razao_social', 'cnpj', 'responsavel']


@admin.register(Instituicao)
class InstituicaoAdmin(admin.ModelAdmin):
    list_display = ['nome_unidade', 'coordenador']
    search_fields = ['nome_unidade', 'coordenador']


@admin.register(RegraValidacao)
class RegraValidacaoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nome', 'severidade_padrao', 'ativa']
    list_filter = ['severidade_padrao', 'ativa']
    search_fields = ['codigo', 'nome', 'descricao']


@admin.register(Estagio)
class EstagioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'empresa', 'curso', 'tipo_estagio', 'carga_horaria_semanal', 'criado_em']
    list_filter = ['tipo_estagio', 'nivel_ensino', 'instituicao']
    search_fields = ['usuario__nome', 'empresa__razao_social', 'curso', 'supervisor_nome']


@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = ['id', 'empresa', 'usuario', 'estagio', 'status', 'score_conformidade', 'versao', 'data_submissao']
    list_filter = ['status', 'instituicao', 'data_submissao']
    search_fields = ['usuario__nome', 'empresa__razao_social']


@admin.register(AnaliseContrato)
class AnaliseContratoAdmin(admin.ModelAdmin):
    list_display = ['id', 'contrato', 'resultado', 'score_conformidade', 'criado_em']
    list_filter = ['resultado', 'criado_em']


@admin.register(Pendencia)
class PendenciaAdmin(admin.ModelAdmin):
    list_display = ['codigo_regra', 'severidade', 'analise', 'resolvida', 'criado_em']
    list_filter = ['severidade', 'resolvida']
    search_fields = ['codigo_regra', 'mensagem']


@admin.register(RelatorioConformidade)
class RelatorioConformidadeAdmin(admin.ModelAdmin):
    list_display = ['analise', 'status', 'gerado_em']
    list_filter = ['status', 'gerado_em']


@admin.register(ParecerInstitucional)
class ParecerInstitucionalAdmin(admin.ModelAdmin):
    list_display = ['contrato', 'instituicao', 'autor', 'aprovado', 'criado_em']
    list_filter = ['aprovado', 'instituicao', 'criado_em']
    search_fields = ['autor', 'observacao']


@admin.register(SistemaValidador)
class SistemaValidadorAdmin(admin.ModelAdmin):
    list_display = ['id', 'contrato']
