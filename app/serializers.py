from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.conf import settings
from django.db import transaction
from rest_framework import serializers

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
    StatusContrato,
    Usuario,
    VersaoContrato,
)
from app.services import PDFExtractionError, extrair_texto_pdf


class UsuarioSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Usuario
        fields = ['id', 'user', 'username', 'cpf', 'nome', 'email']
        read_only_fields = ['id', 'user', 'username']


class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = ['id', 'cnpj', 'razao_social', 'responsavel']
        read_only_fields = ['id']


class InstituicaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instituicao
        fields = ['id', 'nome_unidade', 'coordenador']
        read_only_fields = ['id']


class RegraValidacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegraValidacao
        fields = [
            'id',
            'codigo',
            'nome',
            'descricao',
            'severidade_padrao',
            'ativa',
            'criado_em',
            'atualizado_em',
        ]
        read_only_fields = ['id', 'criado_em', 'atualizado_em']


class EstagioSerializer(serializers.ModelSerializer):
    status_validacao = serializers.CharField(read_only=True)

    class Meta:
        model = Estagio
        fields = [
            'id',
            'usuario',
            'empresa',
            'instituicao',
            'curso',
            'nivel_ensino',
            'tipo_estagio',
            'data_inicio',
            'data_fim',
            'carga_horaria_diaria',
            'carga_horaria_semanal',
            'atividades',
            'supervisor_nome',
            'supervisor_formacao',
            'professor_orientador',
            'seguro_apolice',
            'bolsa_auxilio',
            'auxilio_transporte',
            'plano_atividades',
            'status_validacao',
            'criado_em',
            'atualizado_em',
        ]
        read_only_fields = ['id', 'usuario', 'status_validacao', 'criado_em', 'atualizado_em']

    def validate(self, data):
        data_inicio = data.get('data_inicio', getattr(self.instance, 'data_inicio', None))
        data_fim = data.get('data_fim', getattr(self.instance, 'data_fim', None))
        if data_inicio and data_fim and data_fim < data_inicio:
            raise serializers.ValidationError({'data_fim': 'Data final nao pode ser anterior a data inicial.'})

        for campo in ['carga_horaria_diaria', 'carga_horaria_semanal', 'bolsa_auxilio']:
            valor = data.get(campo)
            if valor is not None and valor < 0:
                raise serializers.ValidationError({campo: 'Valor nao pode ser negativo.'})

        return data


class ContratoSerializer(serializers.ModelSerializer):
    versoes_pdf = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Contrato
        fields = [
            'id',
            'empresa',
            'usuario',
            'instituicao',
            'estagio',
            'data_submissao',
            'versao',
            'arquivo_pdf',
            'status',
            'score_conformidade',
            'versoes_pdf',
        ]
        read_only_fields = ['id', 'usuario', 'data_submissao', 'versao', 'status', 'score_conformidade', 'versoes_pdf']

    def validate_arquivo_pdf(self, arquivo):
        if arquivo and not arquivo.name.lower().endswith('.pdf'):
            raise serializers.ValidationError('O contrato deve ser enviado em formato PDF.')
        if arquivo and getattr(arquivo, 'content_type', None) not in [None, 'application/pdf']:
            raise serializers.ValidationError('O arquivo enviado nao parece ser um PDF.')
        if arquivo and getattr(arquivo, 'size', 0) == 0:
            raise serializers.ValidationError('O arquivo PDF enviado esta vazio.')
        if arquivo and getattr(arquivo, 'size', 0) > settings.CONTRATO_PDF_MAX_SIZE:
            limite_mb = settings.CONTRATO_PDF_MAX_SIZE / (1024 * 1024)
            raise serializers.ValidationError(f'O PDF deve ter no maximo {limite_mb:.0f} MB.')
        if arquivo:
            try:
                extrair_texto_pdf(arquivo)
            except PDFExtractionError as exc:
                raise serializers.ValidationError(exc.messages[0]) from exc
        return arquivo

    def validate_estagio(self, estagio):
        request = self.context.get('request')
        if request and request.user.is_authenticated and not request.user.is_staff:
            perfil = getattr(request.user, 'perfil', None)
            if not perfil or estagio.usuario_id != perfil.id:
                raise serializers.ValidationError('Estagio nao pertence ao usuario autenticado.')
        return estagio

    def update(self, instance, validated_data):
        novo_pdf = validated_data.get('arquivo_pdf')
        if novo_pdf:
            instance.versao = instance.versao + 1 if instance.arquivo_pdf else 1
            instance.status = StatusContrato.RECEBIDO
            instance.score_conformidade = 0.0
        return super().update(instance, validated_data)


class VersaoContratoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VersaoContrato
        fields = ['id', 'contrato', 'arquivo_pdf', 'numero_versao', 'enviado_por', 'criado_em']
        read_only_fields = ['id', 'contrato', 'numero_versao', 'enviado_por', 'criado_em']


class PendenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pendencia
        fields = [
            'id',
            'analise',
            'regra',
            'codigo_regra',
            'severidade',
            'mensagem',
            'resolvida',
            'criado_em',
        ]
        read_only_fields = ['id', 'analise', 'regra', 'codigo_regra', 'severidade', 'mensagem', 'criado_em']


class RelatorioConformidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatorioConformidade
        fields = ['id', 'analise', 'status', 'conteudo', 'gerado_em']
        read_only_fields = ['id', 'gerado_em']


class AnaliseContratoSerializer(serializers.ModelSerializer):
    pendencias = PendenciaSerializer(many=True, read_only=True)
    relatorio = RelatorioConformidadeSerializer(read_only=True)

    class Meta:
        model = AnaliseContrato
        fields = [
            'id',
            'contrato',
            'resultado',
            'score_conformidade',
            'dados_extraidos',
            'observacoes',
            'pendencias',
            'relatorio',
            'criado_em',
        ]
        read_only_fields = ['id', 'resultado', 'score_conformidade', 'pendencias', 'relatorio', 'criado_em']


class ParecerInstitucionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParecerInstitucional
        fields = ['id', 'contrato', 'instituicao', 'autor', 'aprovado', 'observacao', 'criado_em']
        read_only_fields = ['id', 'criado_em']

    def validate(self, data):
        instance = ParecerInstitucional(**data)
        try:
            instance.clean()
        except Exception as exc:
            raise serializers.ValidationError(getattr(exc, 'message_dict', str(exc)))
        return data


class SistemaValidadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = SistemaValidador
        fields = ['id', 'contrato']
        read_only_fields = ['id']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    email = serializers.EmailField(required=True)
    cpf = serializers.CharField(write_only=True, required=True)
    nome = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'cpf', 'nome']
        read_only_fields = ['id']

    @transaction.atomic
    def create(self, validated_data):
        password = validated_data.pop('password')
        cpf = validated_data.pop('cpf')
        nome = validated_data.pop('nome')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        Usuario.objects.create(
            user=user,
            cpf=cpf,
            nome=nome,
            email=user.email,
        )
        return user

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Nome de usuario ja cadastrado.')
        return value

    def validate_email(self, value):
        if value and User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email ja cadastrado.')
        if value and Usuario.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email ja cadastrado em perfil de usuario.')
        return value

    def validate_cpf(self, value):
        if Usuario.objects.filter(cpf=value).exists():
            raise serializers.ValidationError('CPF ja cadastrado.')
        return value


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if not user:
            raise serializers.ValidationError('Credenciais invalidas.')
        return user
