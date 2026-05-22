from datetime import date
from decimal import Decimal

from django.test import TestCase

from app.models import (
    AnaliseContrato,
    Contrato,
    Empresa,
    Estagio,
    Instituicao,
    ParecerInstitucional,
    ResultadoAnalise,
    StatusContrato,
    TipoEstagio,
    Usuario,
)


class AnaliseContratoTests(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(
            cpf='123.456.789-01',
            nome='Alice Santos',
            email='alice@example.com',
        )
        self.empresa = Empresa.objects.create(
            cnpj='12.345.678/0001-91',
            razao_social='TechNova S.A.',
            responsavel='Marcos Lima',
        )
        self.instituicao = Instituicao.objects.create(
            nome_unidade='Ibmec',
            coordenador='Maria Coordenadora',
        )

    def criar_contrato(self, estagio):
        return Contrato.objects.create(
            usuario=self.usuario,
            empresa=self.empresa,
            instituicao=self.instituicao,
            estagio=estagio,
        )

    def test_estagio_regular_gera_analise_aprovada(self):
        estagio = Estagio.objects.create(
            usuario=self.usuario,
            empresa=self.empresa,
            instituicao=self.instituicao,
            curso='Engenharia de Software',
            tipo_estagio=TipoEstagio.OBRIGATORIO,
            data_inicio=date(2026, 1, 1),
            data_fim=date(2026, 12, 31),
            carga_horaria_diaria=Decimal('6.00'),
            carga_horaria_semanal=Decimal('30.00'),
            atividades='Desenvolvimento acompanhado de sistemas internos.',
            supervisor_nome='Carlos Supervisor',
            professor_orientador='Ana Orientadora',
            seguro_apolice='APOLICE-123',
        )
        contrato = self.criar_contrato(estagio)

        analise = AnaliseContrato.gerar_para_contrato(contrato)

        contrato.refresh_from_db()
        self.assertEqual(analise.resultado, ResultadoAnalise.APROVADO)
        self.assertEqual(analise.score_conformidade, 100.0)
        self.assertEqual(analise.pendencias.count(), 0)
        self.assertEqual(contrato.status, StatusContrato.VALIDADO_OK)

    def test_estagio_irregular_gera_pendencias_e_reprova_contrato(self):
        estagio = Estagio.objects.create(
            usuario=self.usuario,
            empresa=self.empresa,
            instituicao=self.instituicao,
            curso='Engenharia de Software',
            tipo_estagio=TipoEstagio.NAO_OBRIGATORIO,
            data_inicio=date(2026, 1, 1),
            data_fim=date(2028, 3, 1),
            carga_horaria_diaria=Decimal('7.00'),
            carga_horaria_semanal=Decimal('35.00'),
        )
        contrato = self.criar_contrato(estagio)

        analise = AnaliseContrato.gerar_para_contrato(contrato)

        contrato.refresh_from_db()
        codigos = set(analise.pendencias.values_list('codigo_regra', flat=True))
        self.assertEqual(analise.resultado, ResultadoAnalise.REPROVADO)
        self.assertEqual(contrato.status, StatusContrato.REPROVADO)
        self.assertTrue({'CARGA_DIARIA', 'CARGA_SEMANAL', 'SEGURO', 'BOLSA', 'AUXILIO_TRANSPORTE'} <= codigos)

    def test_parecer_institucional_atualiza_status_final_do_contrato(self):
        estagio = Estagio.objects.create(
            usuario=self.usuario,
            empresa=self.empresa,
            instituicao=self.instituicao,
            curso='Engenharia de Software',
            tipo_estagio=TipoEstagio.OBRIGATORIO,
            seguro_apolice='APOLICE-123',
            supervisor_nome='Carlos Supervisor',
            professor_orientador='Ana Orientadora',
            atividades='Desenvolvimento acompanhado.',
        )
        contrato = self.criar_contrato(estagio)

        ParecerInstitucional.objects.create(
            contrato=contrato,
            instituicao=self.instituicao,
            autor='Maria Coordenadora',
            aprovado=True,
            observacao='Contrato aprovado pela coordenacao.',
        )

        contrato.refresh_from_db()
        self.assertEqual(contrato.status, StatusContrato.APROVADO_FINAL)
