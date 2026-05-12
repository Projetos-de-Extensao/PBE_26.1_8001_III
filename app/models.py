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
    INVALIDO_PENDENTE = 'INVALIDO_PENDENTE', 'Inválido pendente'
    VALIDADO_OK = 'VALIDADO_OK', 'Validado OK'
    APROVADO_FINAL = 'APROVADO_FINAL', 'Aprovado final'


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


class Contrato(models.Model):
    empresa = models.ForeignKey(Empresa, related_name='contratos', on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, related_name='contratos', on_delete=models.CASCADE)
    instituicao = models.ForeignKey(Instituicao, related_name='contratos', on_delete=models.SET_NULL, null=True, blank=True)
    data_submissao = models.DateTimeField(auto_now_add=True)
    arquivo_original = models.BinaryField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=StatusContrato.choices, default=StatusContrato.RECEBIDO)
    score_conformidade = models.FloatField(default=0.0)

    def __str__(self):
        return f'Contrato {self.id} - {self.empresa}'

    def atualizar_status(self, novo_status):
        self.status = novo_status
        self.save()


class SistemaValidador(models.Model):
    contrato = models.OneToOneField(Contrato, related_name='sistema_validador', on_delete=models.CASCADE)

    def __str__(self):
        return f'Sistema Validador do Contrato {self.contrato.id}'

    def extrair_dados_ocr(self):
        return {}

    def validar_regras(self, dados):
        return 0.0

    def gerar_relatorio_validacao(self):
        return 'Relatório de validação não implementado.'
