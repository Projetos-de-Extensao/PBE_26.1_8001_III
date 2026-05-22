from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from app.models import (
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
from app.serializers import (
    AnaliseContratoSerializer,
    ContratoSerializer,
    EmpresaSerializer,
    EstagioSerializer,
    InstituicaoSerializer,
    ParecerInstitucionalSerializer,
    PendenciaSerializer,
    RegraValidacaoSerializer,
    RelatorioConformidadeSerializer,
    SistemaValidadorSerializer,
    UsuarioSerializer,
)


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer


class InstituicaoViewSet(viewsets.ModelViewSet):
    queryset = Instituicao.objects.all()
    serializer_class = InstituicaoSerializer


class RegraValidacaoViewSet(viewsets.ModelViewSet):
    queryset = RegraValidacao.objects.all()
    serializer_class = RegraValidacaoSerializer


class EstagioViewSet(viewsets.ModelViewSet):
    queryset = Estagio.objects.select_related('usuario', 'empresa', 'instituicao')
    serializer_class = EstagioSerializer


class ContratoViewSet(viewsets.ModelViewSet):
    queryset = Contrato.objects.select_related('usuario', 'empresa', 'instituicao', 'estagio')
    serializer_class = ContratoSerializer

    @action(detail=True, methods=['post'])
    def analisar(self, request, pk=None):
        contrato = self.get_object()
        dados_extraidos = request.data.get('dados_extraidos', {})
        analise = AnaliseContrato.gerar_para_contrato(contrato, dados_extraidos=dados_extraidos)
        serializer = AnaliseContratoSerializer(analise)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AnaliseContratoViewSet(viewsets.ModelViewSet):
    queryset = AnaliseContrato.objects.select_related('contrato').prefetch_related('pendencias')
    serializer_class = AnaliseContratoSerializer


class PendenciaViewSet(viewsets.ModelViewSet):
    queryset = Pendencia.objects.select_related('analise', 'regra')
    serializer_class = PendenciaSerializer


class RelatorioConformidadeViewSet(viewsets.ModelViewSet):
    queryset = RelatorioConformidade.objects.select_related('analise')
    serializer_class = RelatorioConformidadeSerializer


class ParecerInstitucionalViewSet(viewsets.ModelViewSet):
    queryset = ParecerInstitucional.objects.select_related('contrato', 'instituicao')
    serializer_class = ParecerInstitucionalSerializer


class SistemaValidadorViewSet(viewsets.ModelViewSet):
    queryset = SistemaValidador.objects.select_related('contrato')
    serializer_class = SistemaValidadorSerializer
