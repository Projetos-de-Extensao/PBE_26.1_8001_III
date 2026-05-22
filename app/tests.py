from datetime import date
from decimal import Decimal
from pathlib import Path
import shutil

from django.contrib.auth.models import User as AuthUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

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


TEST_MEDIA_ROOT = Path(__file__).resolve().parent.parent / 'test_media'


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


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class ApiWorkflowTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEST_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.client = APIClient()
        self.auth_user = AuthUser.objects.create_user(username='tester', password='senha123')
        self.usuario = Usuario.objects.create(
            cpf='987.654.321-00',
            nome='Bruno Teste',
            email='bruno@example.com',
        )
        self.empresa = Empresa.objects.create(
            cnpj='98.765.432/0001-10',
            razao_social='Empresa Teste',
            responsavel='Responsavel Teste',
        )
        self.instituicao = Instituicao.objects.create(
            nome_unidade='Ibmec Teste',
            coordenador='Coordenador Teste',
        )
        self.estagio = Estagio.objects.create(
            usuario=self.usuario,
            empresa=self.empresa,
            instituicao=self.instituicao,
            curso='Direito',
            tipo_estagio=TipoEstagio.OBRIGATORIO,
            seguro_apolice='APOLICE-999',
            supervisor_nome='Supervisor Teste',
            professor_orientador='Orientador Teste',
            atividades='Atividades juridicas acompanhadas.',
        )
        self.contrato = Contrato.objects.create(
            usuario=self.usuario,
            empresa=self.empresa,
            instituicao=self.instituicao,
            estagio=self.estagio,
        )

    def test_register_endpoint_cria_usuario_django(self):
        response = self.client.post(
            '/api/auth/register/',
            {'username': 'novo', 'email': 'novo@example.com', 'password': 'senha123'},
            format='json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(AuthUser.objects.filter(username='novo').exists())

    def test_contrato_filter_por_status(self):
        response = self.client.get('/api/contratos/', {'status': StatusContrato.RECEBIDO})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.contrato.id)

    def test_upload_pdf_rejeita_arquivo_sem_extensao_pdf(self):
        self.client.force_authenticate(user=self.auth_user)
        arquivo = SimpleUploadedFile('contrato.txt', b'conteudo', content_type='text/plain')

        response = self.client.post(
            f'/api/contratos/{self.contrato.id}/upload-pdf/',
            {'arquivo_pdf': arquivo},
            format='multipart',
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('arquivo_pdf', response.data)

    def test_upload_pdf_aceita_pdf(self):
        self.client.force_authenticate(user=self.auth_user)
        arquivo = SimpleUploadedFile('contrato.pdf', b'%PDF-1.4 conteudo', content_type='application/pdf')

        response = self.client.post(
            f'/api/contratos/{self.contrato.id}/upload-pdf/',
            {'arquivo_pdf': arquivo},
            format='multipart',
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['arquivo_pdf'].endswith('.pdf'))
