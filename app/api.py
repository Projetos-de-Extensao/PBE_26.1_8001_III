from django.contrib.auth import login, logout
from rest_framework import parsers, permissions, status, viewsets
from rest_framework.views import APIView
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
    LoginSerializer,
    ParecerInstitucionalSerializer,
    PendenciaSerializer,
    RegisterSerializer,
    RegraValidacaoSerializer,
    RelatorioConformidadeSerializer,
    SistemaValidadorSerializer,
    UsuarioSerializer,
)


def _aplicar_filtro_id(queryset, params, campo):
    valor = params.get(campo)
    if valor:
        return queryset.filter(**{campo: valor})
    return queryset


def _aplicar_filtro_data(queryset, params, campo):
    data_inicio = params.get('data_inicio')
    data_fim = params.get('data_fim')
    if data_inicio:
        queryset = queryset.filter(**{f'{campo}__date__gte': data_inicio})
    if data_fim:
        queryset = queryset.filter(**{f'{campo}__date__lte': data_fim})
    return queryset


def _param_bool(valor):
    if valor is None:
        return None
    if valor.lower() in ['1', 'true', 'sim', 'yes']:
        return True
    if valor.lower() in ['0', 'false', 'nao', 'não', 'no']:
        return False
    return None


class RegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {'id': user.id, 'username': user.username, 'email': user.email},
            status=status.HTTP_201_CREATED,
        )


class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        login(request, user)
        return Response({'id': user.id, 'username': user.username, 'email': user.email})


class LogoutAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


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
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params
        for campo in ['usuario', 'empresa', 'instituicao', 'tipo_estagio', 'nivel_ensino']:
            queryset = _aplicar_filtro_id(queryset, params, campo)
        curso = params.get('curso')
        if curso:
            queryset = queryset.filter(curso__icontains=curso)
        return queryset


class ContratoViewSet(viewsets.ModelViewSet):
    queryset = Contrato.objects.select_related('usuario', 'empresa', 'instituicao', 'estagio')
    serializer_class = ContratoSerializer
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser, parsers.FormParser]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params
        for campo in ['usuario', 'empresa', 'instituicao', 'estagio', 'status']:
            queryset = _aplicar_filtro_id(queryset, params, campo)
        return _aplicar_filtro_data(queryset, params, 'data_submissao')

    @action(detail=True, methods=['post'])
    def analisar(self, request, pk=None):
        contrato = self.get_object()
        dados_extraidos = request.data.get('dados_extraidos', {})
        analise = AnaliseContrato.gerar_para_contrato(contrato, dados_extraidos=dados_extraidos)
        serializer = AnaliseContratoSerializer(analise)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='upload-pdf', parser_classes=[parsers.MultiPartParser, parsers.FormParser])
    def upload_pdf(self, request, pk=None):
        contrato = self.get_object()
        serializer = self.get_serializer(contrato, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class AnaliseContratoViewSet(viewsets.ModelViewSet):
    queryset = AnaliseContrato.objects.select_related('contrato').prefetch_related('pendencias')
    serializer_class = AnaliseContratoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params
        for campo in ['contrato', 'resultado']:
            queryset = _aplicar_filtro_id(queryset, params, campo)
        return _aplicar_filtro_data(queryset, params, 'criado_em')


class PendenciaViewSet(viewsets.ModelViewSet):
    queryset = Pendencia.objects.select_related('analise', 'regra')
    serializer_class = PendenciaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params
        for campo in ['analise', 'regra', 'codigo_regra', 'severidade']:
            queryset = _aplicar_filtro_id(queryset, params, campo)
        resolvida = _param_bool(params.get('resolvida'))
        if resolvida is not None:
            queryset = queryset.filter(resolvida=resolvida)
        return queryset


class RelatorioConformidadeViewSet(viewsets.ModelViewSet):
    queryset = RelatorioConformidade.objects.select_related('analise')
    serializer_class = RelatorioConformidadeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params
        for campo in ['analise', 'status']:
            queryset = _aplicar_filtro_id(queryset, params, campo)
        return _aplicar_filtro_data(queryset, params, 'gerado_em')


class ParecerInstitucionalViewSet(viewsets.ModelViewSet):
    queryset = ParecerInstitucional.objects.select_related('contrato', 'instituicao')
    serializer_class = ParecerInstitucionalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params
        for campo in ['contrato', 'instituicao']:
            queryset = _aplicar_filtro_id(queryset, params, campo)
        aprovado = _param_bool(params.get('aprovado'))
        if aprovado is not None:
            queryset = queryset.filter(aprovado=aprovado)
        return _aplicar_filtro_data(queryset, params, 'criado_em')


class SistemaValidadorViewSet(viewsets.ModelViewSet):
    queryset = SistemaValidador.objects.select_related('contrato')
    serializer_class = SistemaValidadorSerializer
    permission_classes = [permissions.IsAuthenticated]
