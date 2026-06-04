from decimal import Decimal
import re
from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models


class Usuario(models.Model):
    cpf = models.CharField(max_length=14, unique=True)
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nome


class Empresa(models.Model):
    cnpj = models.CharField(max_length=18, unique=True)
    razao_social = models.CharField(max_length=255)
    responsavel = models.CharField(max_length=100)

    def __str__(self):
        return self.razao_social


class StatusContrato(models.TextChoices):
    RECEBIDO = 'RECEBIDO', 'Recebido'
    PROCESSANDO = 'PROCESSANDO', 'Processando'
    INVALIDO_PENDENTE = 'INVALIDO_PENDENTE', 'Invalido pendente'
    VALIDADO_OK = 'VALIDADO_OK', 'Validado OK'
    APROVADO_FINAL = 'APROVADO_FINAL', 'Aprovado final'
    REPROVADO = 'REPROVADO', 'Reprovado'


class TipoEstagio(models.TextChoices):
    OBRIGATORIO = 'OBRIGATORIO', 'Obrigatorio'
    NAO_OBRIGATORIO = 'NAO_OBRIGATORIO', 'Nao obrigatorio'


class NivelEnsino(models.TextChoices):
    SUPERIOR = 'SUPERIOR', 'Superior'
    MEDIO = 'MEDIO', 'Medio'
    PROFISSIONAL = 'PROFISSIONAL', 'Educacao profissional'
    FUNDAMENTAL_EJA = 'FUNDAMENTAL_EJA', 'Fundamental EJA'


class ResultadoAnalise(models.TextChoices):
    APROVADO = 'APROVADO', 'Aprovado'
    PENDENTE = 'PENDENTE', 'Pendente'
    REPROVADO = 'REPROVADO', 'Reprovado'


class SeveridadePendencia(models.TextChoices):
    INFO = 'INFO', 'Informacao'
    PENDENCIA = 'PENDENCIA', 'Pendencia'
    ERRO = 'ERRO', 'Erro'


class Instituicao(models.Model):
    nome_unidade = models.CharField(max_length=255)
    coordenador = models.CharField(max_length=100)

    def __str__(self):
        return self.nome_unidade

    def analisar_contrato(self, contrato):
        contrato.instituicao = self
        contrato.save()

    def emitir_parecer_final(self, contrato, aprovado: bool):
        contrato.status = StatusContrato.APROVADO_FINAL if aprovado else StatusContrato.INVALIDO_PENDENTE
        contrato.save()


class RegraValidacao(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nome = models.CharField(max_length=120)
    descricao = models.TextField()
    severidade_padrao = models.CharField(
        max_length=20,
        choices=SeveridadePendencia.choices,
        default=SeveridadePendencia.ERRO,
    )
    ativa = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['codigo']

    def __str__(self):
        return f'{self.codigo} - {self.nome}'

    @classmethod
    def defaults(cls):
        return [
            {
                'codigo': 'CARGA_DIARIA',
                'nome': 'Carga horaria diaria',
                'descricao': 'Carga horaria diaria nao deve ultrapassar 6 horas.',
                'severidade_padrao': SeveridadePendencia.ERRO,
            },
            {
                'codigo': 'CARGA_SEMANAL',
                'nome': 'Carga horaria semanal',
                'descricao': 'Carga horaria semanal nao deve ultrapassar 30 horas.',
                'severidade_padrao': SeveridadePendencia.ERRO,
            },
            {
                'codigo': 'SEGURO',
                'nome': 'Seguro obrigatorio',
                'descricao': 'Contrato deve informar seguro contra acidentes pessoais.',
                'severidade_padrao': SeveridadePendencia.ERRO,
            },
            {
                'codigo': 'SUPERVISOR',
                'nome': 'Supervisor da empresa',
                'descricao': 'Contrato deve indicar supervisor da parte concedente.',
                'severidade_padrao': SeveridadePendencia.PENDENCIA,
            },
            {
                'codigo': 'PROFESSOR_ORIENTADOR',
                'nome': 'Professor orientador',
                'descricao': 'Estagio deve ter acompanhamento institucional.',
                'severidade_padrao': SeveridadePendencia.PENDENCIA,
            },
            {
                'codigo': 'ATIVIDADES',
                'nome': 'Plano de atividades',
                'descricao': 'Atividades devem estar descritas para analise de compatibilidade.',
                'severidade_padrao': SeveridadePendencia.PENDENCIA,
            },
            {
                'codigo': 'CURSO',
                'nome': 'Curso',
                'descricao': 'Curso do contrato deve coincidir com o curso cadastrado no estágio.',
                'severidade_padrao': SeveridadePendencia.PENDENCIA,
            },
            {
                'codigo': 'TIPO_ESTAGIO',
                'nome': 'Tipo de estágio',
                'descricao': 'Tipo de estágio do documento deve coincidir com o tipo cadastrado.',
                'severidade_padrao': SeveridadePendencia.PENDENCIA,
            },
            {
                'codigo': 'DATA_INICIO',
                'nome': 'Data de início',
                'descricao': 'Data de início do contrato deve coincidir entre o documento e o cadastro.',
                'severidade_padrao': SeveridadePendencia.PENDENCIA,
            },
            {
                'codigo': 'DATA_FIM',
                'nome': 'Data de fim',
                'descricao': 'Data de fim do contrato deve coincidir entre o documento e o cadastro.',
                'severidade_padrao': SeveridadePendencia.PENDENCIA,
            },
            {
                'codigo': 'BOLSA',
                'nome': 'Bolsa-auxilio',
                'descricao': 'Estagio nao obrigatorio exige bolsa-auxilio.',
                'severidade_padrao': SeveridadePendencia.ERRO,
            },
            {
                'codigo': 'AUXILIO_TRANSPORTE',
                'nome': 'Auxilio-transporte',
                'descricao': 'Estagio nao obrigatorio exige auxilio-transporte.',
                'severidade_padrao': SeveridadePendencia.ERRO,
            },
            {
                'codigo': 'DURACAO_MAXIMA',
                'nome': 'Duracao maxima',
                'descricao': 'Contrato nao deve ultrapassar 2 anos na mesma empresa.',
                'severidade_padrao': SeveridadePendencia.ERRO,
            },
        ]

    @classmethod
    def obter_config(cls, codigo, severidade_padrao):
        regra = cls.objects.filter(codigo=codigo).first()
        if regra and not regra.ativa:
            return None
        return regra or cls(codigo=codigo, severidade_padrao=severidade_padrao)


class Estagio(models.Model):
    usuario = models.ForeignKey(Usuario, related_name='estagios', on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, related_name='estagios', on_delete=models.CASCADE)
    instituicao = models.ForeignKey(Instituicao, related_name='estagios', on_delete=models.SET_NULL, null=True, blank=True)
    curso = models.CharField(max_length=120)
    nivel_ensino = models.CharField(max_length=20, choices=NivelEnsino.choices, default=NivelEnsino.SUPERIOR)
    tipo_estagio = models.CharField(max_length=20, choices=TipoEstagio.choices)
    data_inicio = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)
    carga_horaria_diaria = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    carga_horaria_semanal = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    atividades = models.TextField(blank=True)
    supervisor_nome = models.CharField(max_length=120, blank=True)
    supervisor_formacao = models.CharField(max_length=120, blank=True)
    professor_orientador = models.CharField(max_length=120, blank=True)
    seguro_apolice = models.CharField(max_length=80, blank=True)
    bolsa_auxilio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    auxilio_transporte = models.BooleanField(default=False)
    plano_atividades = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return f'Estagio de {self.usuario} em {self.empresa}'

    def clean(self):
        if self.data_inicio and self.data_fim and self.data_fim < self.data_inicio:
            raise ValidationError({'data_fim': 'Data final nao pode ser anterior a data inicial.'})
        if self.carga_horaria_diaria is not None and self.carga_horaria_diaria < 0:
            raise ValidationError({'carga_horaria_diaria': 'Carga horaria diaria nao pode ser negativa.'})
        if self.carga_horaria_semanal is not None and self.carga_horaria_semanal < 0:
            raise ValidationError({'carga_horaria_semanal': 'Carga horaria semanal nao pode ser negativa.'})
        if self.bolsa_auxilio is not None and self.bolsa_auxilio < 0:
            raise ValidationError({'bolsa_auxilio': 'Bolsa-auxilio nao pode ser negativa.'})

    @property
    def duracao_em_dias(self):
        if not self.data_inicio or not self.data_fim:
            return None
        return (self.data_fim - self.data_inicio).days

    def _pendencia(self, codigo, severidade_padrao, mensagem):
        regra = RegraValidacao.obter_config(codigo, severidade_padrao)
        if regra is None:
            return None
        return {
            'codigo_regra': codigo,
            'regra': regra,
            'severidade': regra.severidade_padrao,
            'mensagem': mensagem,
        }

    def validar_regras_negocio(self):
        pendencias = []

        if self.carga_horaria_diaria is not None and self.carga_horaria_diaria > Decimal('6.00'):
            pendencias.append(self._pendencia(
                'CARGA_DIARIA',
                SeveridadePendencia.ERRO,
                'Carga horaria diaria acima de 6 horas.',
            ))

        if self.carga_horaria_semanal is not None and self.carga_horaria_semanal > Decimal('30.00'):
            pendencias.append(self._pendencia(
                'CARGA_SEMANAL',
                SeveridadePendencia.ERRO,
                'Carga horaria semanal acima de 30 horas.',
            ))

        if not self.seguro_apolice:
            pendencias.append(self._pendencia(
                'SEGURO',
                SeveridadePendencia.ERRO,
                'Seguro contra acidentes pessoais nao informado.',
            ))

        if not self.supervisor_nome:
            pendencias.append(self._pendencia(
                'SUPERVISOR',
                SeveridadePendencia.PENDENCIA,
                'Supervisor da empresa nao informado.',
            ))

        if not self.professor_orientador:
            pendencias.append(self._pendencia(
                'PROFESSOR_ORIENTADOR',
                SeveridadePendencia.PENDENCIA,
                'Professor orientador nao informado.',
            ))

        if not self.atividades and not self.plano_atividades:
            pendencias.append(self._pendencia(
                'ATIVIDADES',
                SeveridadePendencia.PENDENCIA,
                'Atividades ou plano de atividades nao informados.',
            ))

        if self.tipo_estagio == TipoEstagio.NAO_OBRIGATORIO:
            if self.bolsa_auxilio is None or self.bolsa_auxilio <= 0:
                pendencias.append(self._pendencia(
                    'BOLSA',
                    SeveridadePendencia.ERRO,
                    'Estagio nao obrigatorio sem bolsa-auxilio.',
                ))
            if not self.auxilio_transporte:
                pendencias.append(self._pendencia(
                    'AUXILIO_TRANSPORTE',
                    SeveridadePendencia.ERRO,
                    'Estagio nao obrigatorio sem auxilio-transporte.',
                ))

        if self.duracao_em_dias is not None and self.duracao_em_dias > 730:
            pendencias.append(self._pendencia(
                'DURACAO_MAXIMA',
                SeveridadePendencia.ERRO,
                'Duracao do contrato acima de 2 anos.',
            ))

        return [pendencia for pendencia in pendencias if pendencia]

    def status_validacao(self):
        pendencias = self.validar_regras_negocio()
        if any(item['severidade'] == SeveridadePendencia.ERRO for item in pendencias):
            return ResultadoAnalise.REPROVADO
        if pendencias:
            return ResultadoAnalise.PENDENTE
        return ResultadoAnalise.APROVADO


class Contrato(models.Model):
    empresa = models.ForeignKey(Empresa, related_name='contratos', on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, related_name='contratos', on_delete=models.CASCADE)
    instituicao = models.ForeignKey(Instituicao, related_name='contratos', on_delete=models.SET_NULL, null=True, blank=True)
    estagio = models.ForeignKey(Estagio, related_name='contratos', on_delete=models.SET_NULL, null=True, blank=True)
    data_submissao = models.DateTimeField(auto_now_add=True)
    versao = models.PositiveIntegerField(default=1)
    arquivo_original = models.BinaryField(blank=True, null=True)
    arquivo_pdf = models.FileField(upload_to='contratos/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=StatusContrato.choices, default=StatusContrato.RECEBIDO)
    score_conformidade = models.FloatField(default=0.0)

    def __str__(self):
        return f'Contrato {self.id} - {self.empresa}'

    def atualizar_status(self, novo_status):
        self.status = novo_status
        self.save()

    def clean(self):
        if self.arquivo_pdf and not self.arquivo_pdf.name.lower().endswith('.pdf'):
            raise ValidationError({'arquivo_pdf': 'O contrato deve ser enviado em formato PDF.'})

    def save(self, *args, **kwargs):
        if self.estagio:
            self.usuario = self.estagio.usuario
            self.empresa = self.estagio.empresa
            self.instituicao = self.estagio.instituicao
        super().save(*args, **kwargs)


class AnaliseContrato(models.Model):
    contrato = models.ForeignKey(Contrato, related_name='analises', on_delete=models.CASCADE)
    resultado = models.CharField(max_length=20, choices=ResultadoAnalise.choices, default=ResultadoAnalise.PENDENTE)
    score_conformidade = models.FloatField(default=0.0)
    dados_extraidos = models.JSONField(default=dict, blank=True)
    observacoes = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return f'Analise {self.id} - contrato {self.contrato_id}'

    @classmethod
    def _normalizar_str(cls, valor):
        if valor is None:
            return None
        return str(valor).strip().lower()

    @classmethod
    def _valores_iguais(cls, valor_pdf, valor_estagio):
        if valor_pdf is None or valor_estagio is None:
            return False
        if isinstance(valor_pdf, str) or isinstance(valor_estagio, str):
            return cls._normalizar_str(valor_pdf) == cls._normalizar_str(valor_estagio)
        return valor_pdf == valor_estagio

    @classmethod
    def _pendencia_por_comparacao(cls, codigo, severidade_padrao, mensagem):
        regra = RegraValidacao.obter_config(codigo, severidade_padrao)
        if regra is None:
            return None
        return {
            'codigo_regra': codigo,
            'regra': regra,
            'severidade': regra.severidade_padrao,
            'mensagem': mensagem,
        }

    @classmethod
    def _comparar_dados_extraidos(cls, estagio, dados_extraidos):
        if not dados_extraidos:
            return []

        pendencias = []
        if dados_extraidos.get('curso') and estagio.curso:
            if not cls._valores_iguais(dados_extraidos.get('curso'), estagio.curso):
                pendencias.append(cls._pendencia_por_comparacao(
                    'CURSO',
                    SeveridadePendencia.PENDENCIA,
                    'Curso do documento diverge do curso cadastrado no estágio.',
                ))

        if dados_extraidos.get('tipo_estagio') and estagio.tipo_estagio:
            if not cls._valores_iguais(dados_extraidos.get('tipo_estagio'), estagio.tipo_estagio):
                pendencias.append(cls._pendencia_por_comparacao(
                    'TIPO_ESTAGIO',
                    SeveridadePendencia.PENDENCIA,
                    'Tipo de estágio do documento diverge do tipo cadastrado.',
                ))

        if dados_extraidos.get('data_inicio') and estagio.data_inicio:
            if not cls._valores_iguais(dados_extraidos.get('data_inicio'), estagio.data_inicio):
                pendencias.append(cls._pendencia_por_comparacao(
                    'DATA_INICIO',
                    SeveridadePendencia.PENDENCIA,
                    'Data de início do documento diverge da data cadastrada.',
                ))

        if dados_extraidos.get('data_fim') and estagio.data_fim:
            if not cls._valores_iguais(dados_extraidos.get('data_fim'), estagio.data_fim):
                pendencias.append(cls._pendencia_por_comparacao(
                    'DATA_FIM',
                    SeveridadePendencia.PENDENCIA,
                    'Data de fim do documento diverge da data cadastrada.',
                ))

        if dados_extraidos.get('carga_horaria_diaria') is not None and estagio.carga_horaria_diaria is not None:
            if not cls._valores_iguais(dados_extraidos.get('carga_horaria_diaria'), estagio.carga_horaria_diaria):
                pendencias.append(cls._pendencia_por_comparacao(
                    'CARGA_DIARIA',
                    SeveridadePendencia.ERRO,
                    'Carga horaria diaria do documento diverge do cadastro.',
                ))

        if dados_extraidos.get('carga_horaria_semanal') is not None and estagio.carga_horaria_semanal is not None:
            if not cls._valores_iguais(dados_extraidos.get('carga_horaria_semanal'), estagio.carga_horaria_semanal):
                pendencias.append(cls._pendencia_por_comparacao(
                    'CARGA_SEMANAL',
                    SeveridadePendencia.ERRO,
                    'Carga horaria semanal do documento diverge do cadastro.',
                ))

        if dados_extraidos.get('seguro_apolice') and estagio.seguro_apolice:
            if not cls._valores_iguais(dados_extraidos.get('seguro_apolice'), estagio.seguro_apolice):
                pendencias.append(cls._pendencia_por_comparacao(
                    'SEGURO',
                    SeveridadePendencia.ERRO,
                    'Numero de apolice de seguro diverge do cadastro.',
                ))

        if dados_extraidos.get('supervisor_nome') and estagio.supervisor_nome:
            if not cls._valores_iguais(dados_extraidos.get('supervisor_nome'), estagio.supervisor_nome):
                pendencias.append(cls._pendencia_por_comparacao(
                    'SUPERVISOR',
                    SeveridadePendencia.PENDENCIA,
                    'Nome do supervisor no documento diverge do cadastro.',
                ))

        if dados_extraidos.get('professor_orientador') and estagio.professor_orientador:
            if not cls._valores_iguais(dados_extraidos.get('professor_orientador'), estagio.professor_orientador):
                pendencias.append(cls._pendencia_por_comparacao(
                    'PROFESSOR_ORIENTADOR',
                    SeveridadePendencia.PENDENCIA,
                    'Professor orientador no documento diverge do cadastro.',
                ))

        if dados_extraidos.get('bolsa_auxilio') is not None and estagio.bolsa_auxilio is not None:
            if not cls._valores_iguais(dados_extraidos.get('bolsa_auxilio'), estagio.bolsa_auxilio):
                pendencias.append(cls._pendencia_por_comparacao(
                    'BOLSA',
                    SeveridadePendencia.ERRO,
                    'Valor de bolsa-auxilio no documento diverge do cadastro.',
                ))

        if dados_extraidos.get('auxilio_transporte') is not None and estagio.auxilio_transporte is not None:
            if not cls._valores_iguais(dados_extraidos.get('auxilio_transporte'), estagio.auxilio_transporte):
                pendencias.append(cls._pendencia_por_comparacao(
                    'AUXILIO_TRANSPORTE',
                    SeveridadePendencia.ERRO,
                    'Valor de auxilio-transporte no documento diverge do cadastro.',
                ))

        return [pendencia for pendencia in pendencias if pendencia]

    @classmethod
    def gerar_para_contrato(cls, contrato, dados_extraidos=None):
        if dados_extraidos is None:
            dados_extraidos = {}
            try:
                sistema = contrato.sistema_validador
            except Exception:
                sistema = None
            if sistema:
                dados_extraidos = sistema.extrair_dados_ocr() or {}

        analise = cls.objects.create(contrato=contrato, dados_extraidos=dados_extraidos)

        if not contrato.estagio:
            Pendencia.objects.create(
                analise=analise,
                codigo_regra='ESTAGIO',
                severidade=SeveridadePendencia.PENDENCIA,
                mensagem='Contrato sem cadastro de estagio vinculado.',
            )
        else:
            comparacoes = contrato.estagio.validar_regras_negocio()
            comparacoes.extend(cls._comparar_dados_extraidos(contrato.estagio, dados_extraidos))
            for item in comparacoes:
                if not item:
                    continue
                Pendencia.objects.create(
                    analise=analise,
                    regra=item['regra'] if getattr(item['regra'], 'pk', None) else None,
                    codigo_regra=item['codigo_regra'],
                    severidade=item['severidade'],
                    mensagem=item['mensagem'],
                )

        analise.recalcular_resultado()
        RelatorioConformidade.objects.create(
            analise=analise,
            status=analise.resultado,
            conteudo=analise.resumo_textual(),
        )
        return analise

    def recalcular_resultado(self):
        pendencias = self.pendencias.all()
        total_pendencias = pendencias.count()
        total_erros = pendencias.filter(severidade=SeveridadePendencia.ERRO).count()

        if total_erros:
            self.resultado = ResultadoAnalise.REPROVADO
        elif total_pendencias:
            self.resultado = ResultadoAnalise.PENDENTE
        else:
            self.resultado = ResultadoAnalise.APROVADO

        self.score_conformidade = max(0.0, 100.0 - (total_erros * 20.0) - ((total_pendencias - total_erros) * 10.0))
        self.save(update_fields=['resultado', 'score_conformidade'])

        contrato_status = {
            ResultadoAnalise.APROVADO: StatusContrato.VALIDADO_OK,
            ResultadoAnalise.PENDENTE: StatusContrato.INVALIDO_PENDENTE,
            ResultadoAnalise.REPROVADO: StatusContrato.REPROVADO,
        }[self.resultado]
        self.contrato.status = contrato_status
        self.contrato.score_conformidade = self.score_conformidade
        self.contrato.save(update_fields=['status', 'score_conformidade'])

    def resumo_textual(self):
        linhas = [
            f'Resultado: {self.resultado}',
            f'Score de conformidade: {self.score_conformidade:.1f}',
        ]
        for pendencia in self.pendencias.all():
            linhas.append(f'- [{pendencia.severidade}] {pendencia.mensagem}')
        return '\n'.join(linhas)


class Pendencia(models.Model):
    analise = models.ForeignKey(AnaliseContrato, related_name='pendencias', on_delete=models.CASCADE)
    regra = models.ForeignKey(RegraValidacao, related_name='pendencias', on_delete=models.SET_NULL, null=True, blank=True)
    codigo_regra = models.CharField(max_length=50)
    severidade = models.CharField(max_length=20, choices=SeveridadePendencia.choices)
    mensagem = models.TextField()
    resolvida = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['severidade', 'codigo_regra']

    def __str__(self):
        return f'{self.codigo_regra} - {self.severidade}'


class RelatorioConformidade(models.Model):
    analise = models.OneToOneField(AnaliseContrato, related_name='relatorio', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=ResultadoAnalise.choices)
    conteudo = models.TextField()
    gerado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Relatorio da analise {self.analise_id}'


class ParecerInstitucional(models.Model):
    contrato = models.ForeignKey(Contrato, related_name='pareceres', on_delete=models.CASCADE)
    instituicao = models.ForeignKey(Instituicao, related_name='pareceres', on_delete=models.CASCADE)
    autor = models.CharField(max_length=120)
    aprovado = models.BooleanField()
    observacao = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return f'Parecer {self.id} - contrato {self.contrato_id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.contrato.instituicao = self.instituicao
        self.contrato.status = StatusContrato.APROVADO_FINAL if self.aprovado else StatusContrato.INVALIDO_PENDENTE
        self.contrato.save(update_fields=['instituicao', 'status'])


class SistemaValidador(models.Model):
    contrato = models.OneToOneField(Contrato, related_name='sistema_validador', on_delete=models.CASCADE)

    def __str__(self):
        return f'Sistema Validador do Contrato {self.contrato.id}'

    def extrair_dados_ocr(self):
        return {}

    def validar_regras(self, dados):
        analise = AnaliseContrato.gerar_para_contrato(self.contrato, dados_extraidos=dados)
        return analise.score_conformidade

    def gerar_relatorio_validacao(self):
        analise = self.contrato.analises.first()
        if not analise:
            analise = AnaliseContrato.gerar_para_contrato(self.contrato)
        return analise.relatorio.conteudo

    def extrair_dados_ocr(self):
        if not self.contrato.arquivo_pdf:
            return {}

        try:
            with self.contrato.arquivo_pdf.open('rb') as arquivo:
                import pdfplumber
                with pdfplumber.open(arquivo) as pdf:
                    texto = '\n'.join(page.extract_text() or '' for page in pdf.pages)
        except Exception:
            return {}

        return self._extrair_dados_do_texto(texto)

    def _extrair_dados_do_texto(self, texto):
        texto = texto or ''

        dados = {
            'cpf': self._buscar_regex(texto, r'\bcpf[:\s]*([0-9\.\-]+)'),
            'cnpj': self._buscar_regex(texto, r'\bcnpj[:\s]*([0-9\./\-]+)'),
            'curso': self._buscar_regex(texto, r'\bcurso[:\s]*([^\n]+)'),
            'tipo_estagio': self._parse_tipo_estagio(self._buscar_regex(texto, r'\btipo\s+de\s+estagi[oó][:\s]*([^\n]+)')),
            'data_inicio': self._parse_data(self._buscar_regex(texto, r'\bdata(?:\s+de)?\s+in[ií]cio[:\s]*([0-9/\-]+)')),
            'data_fim': self._parse_data(self._buscar_regex(texto, r'\bdata(?:\s+de)?\s+fim[:\s]*([0-9/\-]+)')),
            'carga_horaria_diaria': self._parse_decimal(self._buscar_regex(texto, r'\bcarga\s+hor[aá]ria\s+di[aá]ria[:\s]*([0-9\.,]+)')),
            'carga_horaria_semanal': self._parse_decimal(self._buscar_regex(texto, r'\bcarga\s+hor[aá]ria\s+semanal[:\s]*([0-9\.,]+)')),
            'seguro_apolice': self._buscar_regex(texto, r'\bseguro(?:\s+ap[oó]lice)?[:\s]*([^\n]+)'),
            'supervisor_nome': self._buscar_regex(texto, r'\bsupervisor(?:\s+nome)?[:\s]*([^\n]+)'),
            'professor_orientador': self._buscar_regex(texto, r'\bprofessor\s+orientador[:\s]*([^\n]+)'),
            'bolsa_auxilio': self._parse_decimal(self._buscar_regex(texto, r'\bbolsa(?:\s+aux[ií]lio)?[:\s]*([0-9\.,]+)')),
            'auxilio_transporte': self._parse_bool(self._buscar_regex(texto, r'\baux[ií]lio(?:\s+transporte)?[:\s]*(sim|nao|não|true|false|1|0)')),
            'atividades': self._buscar_regex(texto, r'\batividades[:\s]*([^\n]+)'),
            'plano_atividades': self._buscar_regex(texto, r'\bplano\s+de\s+atividades[:\s]*([^\n]+)'),
        }

        return {k: v for k, v in dados.items() if v is not None}

    def _buscar_regex(self, texto, padrao):
        match = re.search(padrao, texto, flags=re.I | re.M)
        return match.group(1).strip() if match else None

    def _parse_data(self, valor):
        if not valor:
            return None
        valor = valor.strip().replace(' ', '')
        for fmt in ('%d/%m/%Y', '%d/%m/%y', '%Y-%m-%d'):
            try:
                return datetime.strptime(valor, fmt).date()
            except ValueError:
                continue
        return None

    def _parse_decimal(self, valor):
        if not valor:
            return None
        normalized = valor.replace('.', '').replace(',', '.')
        try:
            return Decimal(normalized)
        except Exception:
            return None

    def _parse_bool(self, valor):
        if not valor:
            return None
        valor = valor.strip().lower()
        if valor in ('sim', 's', 'true', 'verdadeiro', '1'):
            return True
        if valor in ('nao', 'não', 'n', 'false', 'f', '0'):
            return False
        return None

    def _parse_tipo_estagio(self, valor):
        if not valor:
            return None
        texto = valor.strip().lower()
        if 'obrig' in texto:
            return TipoEstagio.OBRIGATORIO
        if 'nao' in texto or 'não' in texto:
            return TipoEstagio.NAO_OBRIGATORIO
        return None
