from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.api import (
    AnaliseContratoViewSet,
    ContratoViewSet,
    EmpresaViewSet,
    EstagioViewSet,
    InstituicaoViewSet,
    ParecerInstitucionalViewSet,
    PendenciaViewSet,
    RegraValidacaoViewSet,
    RelatorioConformidadeViewSet,
    SistemaValidadorViewSet,
    UsuarioViewSet,
)


router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'empresas', EmpresaViewSet, basename='empresa')
router.register(r'instituicoes', InstituicaoViewSet, basename='instituicao')
router.register(r'regras-validacao', RegraValidacaoViewSet, basename='regra-validacao')
router.register(r'estagios', EstagioViewSet, basename='estagio')
router.register(r'contratos', ContratoViewSet, basename='contrato')
router.register(r'analises', AnaliseContratoViewSet, basename='analise-contrato')
router.register(r'pendencias', PendenciaViewSet, basename='pendencia')
router.register(r'relatorios', RelatorioConformidadeViewSet, basename='relatorio-conformidade')
router.register(r'pareceres', ParecerInstitucionalViewSet, basename='parecer-institucional')
router.register(r'sistemas-validadores', SistemaValidadorViewSet, basename='sistema-validador')

urlpatterns = [
    path('', include(router.urls)),
]
