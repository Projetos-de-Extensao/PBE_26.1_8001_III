from django.contrib.auth import login, logout
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db.models import Avg, Count
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
    StatusContrato,
    SistemaValidador,
    Usuario,
    VersaoContrato,
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


def _perfil_usuario(user):
    return getattr(user, 'perfil', None)


def _exigir_perfil(user):
    perfil = _perfil_usuario(user)
    if not perfil:
        raise DjangoValidationError('Usuario autenticado nao possui perfil de dominio vinculado.')
    return perfil


class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return bool(request.user and request.user.is_staff)


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
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        if self.request.user.is_staff:
            serializer.save()
            return
        if _perfil_usuario(self.request.user):
            raise DjangoValidationError('Usuario autenticado ja possui perfil de dominio.')
        serializer.save(user=self.request.user)


class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        perfil = _perfil_usuario(self.request.user)
        if not perfil:
            return queryset.none()
        return queryset.filter(estagios__usuario=perfil).distinct()


class InstituicaoViewSet(viewsets.ModelViewSet):
    queryset = Instituicao.objects.all()
    serializer_class = InstituicaoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        perfil = _perfil_usuario(self.request.user)
        if not perfil:
            return queryset.none()
        return queryset.filter(estagios__usuario=perfil).distinct()


class RegraValidacaoViewSet(viewsets.ModelViewSet):
    queryset = RegraValidacao.objects.all()
    serializer_class = RegraValidacaoSerializer
    permission_classes = [IsStaffOrReadOnly]


class EstagioViewSet(viewsets.ModelViewSet):
    queryset = Estagio.objects.select_related('usuario', 'empresa', 'instituicao')
    serializer_class = EstagioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            perfil = _perfil_usuario(self.request.user)
            if not perfil:
                return queryset.none()
            queryset = queryset.filter(usuario=perfil)
        params = self.request.query_params
        for campo in ['usuario', 'empresa', 'instituicao', 'tipo_estagio', 'nivel_ensino']:
            queryset = _aplicar_filtro_id(queryset, params, campo)
        curso = params.get('curso')
        if curso:
            queryset = queryset.filter(curso__icontains=curso)
        return queryset

    def perform_create(self, serializer):
        perfil = _exigir_perfil(self.request.user)
        serializer.save(usuario=perfil)


class ContratoViewSet(viewsets.ModelViewSet):
    queryset = Contrato.objects.select_related('usuario', 'empresa', 'instituicao', 'estagio')
    serializer_class = ContratoSerializer
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser, parsers.FormParser]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            perfil = _perfil_usuario(self.request.user)
            if not perfil:
                return queryset.none()
            queryset = queryset.filter(usuario=perfil)
        params = self.request.query_params
        for campo in ['usuario', 'empresa', 'instituicao', 'estagio', 'status']:
            queryset = _aplicar_filtro_id(queryset, params, campo)
        return _aplicar_filtro_data(queryset, params, 'data_submissao')

    def perform_create(self, serializer):
        if self.request.user.is_staff:
            serializer.save()
            return
        perfil = _exigir_perfil(self.request.user)
        serializer.save(usuario=perfil)

    @action(detail=True, methods=['post'])
    def analisar(self, request, pk=None):
        contrato = self.get_object()
        dados_extraidos = request.data.get('dados_extraidos')
        try:
            if dados_extraidos is None:
                sistema, _ = SistemaValidador.objects.get_or_create(contrato=contrato)
                dados_extraidos = sistema.extrair_dados_ocr()
            analise = AnaliseContrato.gerar_para_contrato(contrato, dados_extraidos=dados_extraidos)
        except DjangoValidationError as exc:
            mensagem = exc.messages[0] if getattr(exc, 'messages', None) else str(exc)
            return Response({'detail': mensagem}, status=status.HTTP_400_BAD_REQUEST)
        serializer = AnaliseContratoSerializer(analise)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='upload-pdf', parser_classes=[parsers.MultiPartParser, parsers.FormParser])
    def upload_pdf(self, request, pk=None):
        contrato = self.get_object()
        serializer = self.get_serializer(contrato, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        contrato = serializer.save()
        if contrato.arquivo_pdf:
            VersaoContrato.objects.create(
                contrato=contrato,
                arquivo_pdf=contrato.arquivo_pdf.name,
                numero_versao=contrato.versao,
                enviado_por=request.user if request.user.is_authenticated else None,
            )
        return Response(serializer.data)


class AnaliseContratoViewSet(viewsets.ModelViewSet):
    queryset = AnaliseContrato.objects.select_related('contrato').prefetch_related('pendencias')
    serializer_class = AnaliseContratoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            perfil = _perfil_usuario(self.request.user)
            if not perfil:
                return queryset.none()
            queryset = queryset.filter(contrato__usuario=perfil)
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
        if not self.request.user.is_staff:
            perfil = _perfil_usuario(self.request.user)
            if not perfil:
                return queryset.none()
            queryset = queryset.filter(analise__contrato__usuario=perfil)
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
        if not self.request.user.is_staff:
            perfil = _perfil_usuario(self.request.user)
            if not perfil:
                return queryset.none()
            queryset = queryset.filter(analise__contrato__usuario=perfil)
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
        if not self.request.user.is_staff:
            perfil = _perfil_usuario(self.request.user)
            if not perfil:
                return queryset.none()
            queryset = queryset.filter(contrato__usuario=perfil)
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

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        perfil = _perfil_usuario(self.request.user)
        if not perfil:
            return queryset.none()
        return queryset.filter(contrato__usuario=perfil)


class MeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        perfil = _perfil_usuario(request.user)
        return Response({
            'id': request.user.id,
            'username': request.user.username,
            'email': request.user.email,
            'is_staff': request.user.is_staff,
            'perfil': UsuarioSerializer(perfil).data if perfil else None,
        })


class DashboardAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        contratos = Contrato.objects.all()
        pendencias = Pendencia.objects.filter(resolvida=False)

        if not request.user.is_staff:
            perfil = _perfil_usuario(request.user)
            if not perfil:
                contratos = contratos.none()
                pendencias = pendencias.none()
            else:
                contratos = contratos.filter(usuario=perfil)
                pendencias = pendencias.filter(analise__contrato__usuario=perfil)

        pendencias_mais_comuns = (
            pendencias.values('codigo_regra')
            .annotate(total=Count('id'))
            .order_by('-total', 'codigo_regra')[:5]
        )

        return Response({
            'total_contratos': contratos.count(),
            'contratos_recebidos': contratos.filter(status=StatusContrato.RECEBIDO).count(),
            'contratos_pendentes': contratos.filter(status=StatusContrato.INVALIDO_PENDENTE).count(),
            'contratos_aprovados': contratos.filter(status=StatusContrato.APROVADO_FINAL).count(),
            'contratos_reprovados': contratos.filter(status=StatusContrato.REPROVADO).count(),
            'media_score_conformidade': contratos.aggregate(media=Avg('score_conformidade'))['media'] or 0.0,
            'pendencias_mais_comuns': list(pendencias_mais_comuns),
        })
