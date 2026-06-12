from datetime import date
from decimal import Decimal
from pathlib import Path
import shutil

from django.contrib.auth.models import User as AuthUser
from django.core.exceptions import ValidationError
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
    Pendencia,
    ResultadoAnalise,
    SeveridadePendencia,
    StatusContrato,
    TipoEstagio,
    Usuario,
    VersaoContrato,
)


MINIMAL_PDF_BYTES = b"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>
endobj
4 0 obj
<< /Length 73 >>
stream
BT
/F1 12 Tf
72 720 Td
(CPF: 123.456.789-01) Tj
0 -14 Td
(CNPJ: 12.345.678/0001-91) Tj
ET
endstream
endobj
5 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj
xref
0 6
0000000000 65535 f 
0000000010 00000 n 
0000000060 00000 n 
0000000121 00000 n 
0000000210 00000 n 
0000000295 00000 n 
trailer
<< /Root 1 0 R /Size 6 >>
startxref
378
%%EOF
"""

TEST_MEDIA_ROOT = Path(__file__).resolve().parent.parent / 'test_media'


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class BackendHardeningTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEST_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.client = APIClient()
        self.auth_user = AuthUser.objects.create_user(username='alice', email='alice@example.com', password='senha123')
        self.outro_auth_user = AuthUser.objects.create_user(username='bob', email='bob@example.com', password='senha123')
        self.admin = AuthUser.objects.create_superuser(username='admin', email='admin@example.com', password='senha123')
        self.usuario = Usuario.objects.create(
            user=self.auth_user,
            cpf='123.456.789-01',
            nome='Alice Santos',
            email='alice@example.com',
        )
        self.outro_usuario = Usuario.objects.create(
            user=self.outro_auth_user,
            cpf='987.654.321-00',
            nome='Bob Costa',
            email='bob@example.com',
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
        self.estagio = self.criar_estagio(self.usuario)
        self.outro_estagio = self.criar_estagio(self.outro_usuario)
        self.contrato = Contrato.objects.create(
            usuario=self.usuario,
            empresa=self.empresa,
            instituicao=self.instituicao,
            estagio=self.estagio,
        )
        self.outro_contrato = Contrato.objects.create(
            usuario=self.outro_usuario,
            empresa=self.empresa,
            instituicao=self.instituicao,
            estagio=self.outro_estagio,
        )

    def criar_estagio(self, usuario):
        return Estagio.objects.create(
            usuario=usuario,
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

    def pdf_upload(self, nome='contrato.pdf', conteudo=MINIMAL_PDF_BYTES, content_type='application/pdf'):
        return SimpleUploadedFile(nome, conteudo, content_type=content_type)

    def test_usuario_comum_nao_acessa_contrato_de_outro_usuario(self):
        self.client.force_authenticate(user=self.auth_user)

        response = self.client.get(f'/api/contratos/{self.outro_contrato.id}/')

        self.assertEqual(response.status_code, 404)

    def test_admin_acessa_todos_os_contratos(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.get('/api/contratos/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_usuario_nao_autenticado_nao_acessa_dados_sensiveis(self):
        endpoints = [
            '/api/contratos/',
            '/api/estagios/',
            '/api/analises/',
            '/api/pendencias/',
            '/api/relatorios/',
            '/api/me/',
            '/api/dashboard/',
        ]

        for endpoint in endpoints:
            with self.subTest(endpoint=endpoint):
                response = self.client.get(endpoint)
                self.assertIn(response.status_code, [401, 403])

    def test_admin_consegue_editar_recurso_administrativo(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.patch(
            f'/api/empresas/{self.empresa.id}/',
            {'responsavel': 'Responsavel Admin'},
            format='json',
        )

        self.empresa.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.empresa.responsavel, 'Responsavel Admin')

    def test_usuario_comum_nao_cria_analise_direta(self):
        self.client.force_authenticate(user=self.auth_user)

        response = self.client.post('/api/analises/', {'contrato': self.contrato.id}, format='json')

        self.assertEqual(response.status_code, 405)

    def test_usuario_comum_nao_cria_relatorio_direto(self):
        self.client.force_authenticate(user=self.auth_user)
        analise = AnaliseContrato.objects.create(contrato=self.contrato)

        response = self.client.post(
            '/api/relatorios/',
            {'analise': analise.id, 'status': ResultadoAnalise.APROVADO, 'conteudo': 'ok'},
            format='json',
        )

        self.assertEqual(response.status_code, 405)

    def test_usuario_comum_nao_cria_sistema_validador_direto(self):
        self.client.force_authenticate(user=self.auth_user)

        response = self.client.post('/api/sistemas-validadores/', {'contrato': self.contrato.id}, format='json')

        self.assertEqual(response.status_code, 405)

    def test_usuario_comum_nao_cria_parecer_para_contrato_de_outro_usuario(self):
        self.client.force_authenticate(user=self.auth_user)

        response = self.client.post(
            '/api/pareceres/',
            {
                'contrato': self.outro_contrato.id,
                'instituicao': self.instituicao.id,
                'autor': 'Alice',
                'aprovado': True,
            },
            format='json',
        )

        self.assertEqual(response.status_code, 403)

    def test_usuario_comum_nao_edita_empresa_ou_instituicao(self):
        self.client.force_authenticate(user=self.auth_user)

        empresa_response = self.client.patch(
            f'/api/empresas/{self.empresa.id}/',
            {'responsavel': 'Outro'},
            format='json',
        )
        instituicao_response = self.client.patch(
            f'/api/instituicoes/{self.instituicao.id}/',
            {'coordenador': 'Outro'},
            format='json',
        )

        self.assertEqual(empresa_response.status_code, 403)
        self.assertEqual(instituicao_response.status_code, 403)

    def test_upload_pdf_valido(self):
        self.client.force_authenticate(user=self.auth_user)

        response = self.client.post(
            f'/api/contratos/{self.contrato.id}/upload-pdf/',
            {'arquivo_pdf': self.pdf_upload()},
            format='multipart',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['versao'], 1)
        self.assertTrue(response.data['arquivo_pdf'].endswith('.pdf'))
        self.assertEqual(self.contrato.versoes_pdf.count(), 1)
        versao = self.contrato.versoes_pdf.get(numero_versao=1)
        self.contrato.refresh_from_db()
        self.assertNotEqual(versao.arquivo_pdf.name, self.contrato.arquivo_pdf.name)
        self.assertTrue(versao.arquivo_pdf.name.startswith('contratos/versoes/'))

    def test_rejeita_pdf_invalido_corrompido(self):
        self.client.force_authenticate(user=self.auth_user)

        response = self.client.post(
            f'/api/contratos/{self.contrato.id}/upload-pdf/',
            {'arquivo_pdf': self.pdf_upload(conteudo=b'nao sou pdf')},
            format='multipart',
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('errors', response.data)

    def test_rejeita_pdf_vazio(self):
        self.client.force_authenticate(user=self.auth_user)

        response = self.client.post(
            f'/api/contratos/{self.contrato.id}/upload-pdf/',
            {'arquivo_pdf': self.pdf_upload(conteudo=b'')},
            format='multipart',
        )

        self.contrato.refresh_from_db()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.contrato.versoes_pdf.count(), 0)

    @override_settings(CONTRATO_PDF_MAX_SIZE=10)
    def test_rejeita_pdf_acima_do_tamanho_maximo(self):
        self.client.force_authenticate(user=self.auth_user)

        response = self.client.post(
            f'/api/contratos/{self.contrato.id}/upload-pdf/',
            {'arquivo_pdf': self.pdf_upload(conteudo=MINIMAL_PDF_BYTES)},
            format='multipart',
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.contrato.versoes_pdf.count(), 0)

    def test_upload_corrompido_nao_altera_versao_ou_status(self):
        self.client.force_authenticate(user=self.auth_user)

        response = self.client.post(
            f'/api/contratos/{self.contrato.id}/upload-pdf/',
            {'arquivo_pdf': self.pdf_upload(conteudo=b'nao sou pdf')},
            format='multipart',
        )

        self.contrato.refresh_from_db()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.contrato.versao, 1)
        self.assertEqual(self.contrato.status, StatusContrato.RECEBIDO)
        self.assertEqual(self.contrato.versoes_pdf.count(), 0)

    def test_upload_sem_arquivo_nao_cria_nova_versao(self):
        self.client.force_authenticate(user=self.auth_user)

        response = self.client.post(
            f'/api/contratos/{self.contrato.id}/upload-pdf/',
            {},
            format='multipart',
        )

        self.contrato.refresh_from_db()
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.data)
        self.assertEqual(self.contrato.versao, 1)
        self.assertEqual(self.contrato.versoes_pdf.count(), 0)

    def test_incrementa_versao_no_reenvio(self):
        self.client.force_authenticate(user=self.auth_user)
        self.client.post(
            f'/api/contratos/{self.contrato.id}/upload-pdf/',
            {'arquivo_pdf': self.pdf_upload('contrato-v1.pdf')},
            format='multipart',
        )

        response = self.client.post(
            f'/api/contratos/{self.contrato.id}/upload-pdf/',
            {'arquivo_pdf': self.pdf_upload('contrato-v2.pdf')},
            format='multipart',
        )

        self.contrato.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.contrato.versao, 2)
        self.assertEqual(self.contrato.status, StatusContrato.RECEBIDO)
        self.assertEqual(self.contrato.versoes_pdf.count(), 2)
        self.assertTrue(self.contrato.versoes_pdf.filter(numero_versao=1).exists())
        self.assertTrue(self.contrato.versoes_pdf.filter(numero_versao=2).exists())

    def test_analise_automatica_usando_pdf(self):
        self.client.force_authenticate(user=self.auth_user)
        self.client.post(
            f'/api/contratos/{self.contrato.id}/upload-pdf/',
            {'arquivo_pdf': self.pdf_upload()},
            format='multipart',
        )

        response = self.client.post(f'/api/contratos/{self.contrato.id}/analisar/', format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['dados_extraidos']['cpf'], '123.456.789-01')
        self.assertEqual(response.data['dados_extraidos']['cnpj'], '12.345.678/0001-91')

    def test_transicao_invalida_de_status_e_bloqueada(self):
        with self.assertRaises(ValidationError):
            self.contrato.atualizar_status(StatusContrato.APROVADO_FINAL)

    def test_parecer_institucional_so_funciona_em_status_permitido(self):
        with self.assertRaises(ValidationError):
            ParecerInstitucional.objects.create(
                contrato=self.contrato,
                instituicao=self.instituicao,
                autor='Maria Coordenadora',
                aprovado=True,
            )

        AnaliseContrato.gerar_para_contrato(self.contrato, dados_extraidos={})
        ParecerInstitucional.objects.create(
            contrato=self.contrato,
            instituicao=self.instituicao,
            autor='Maria Coordenadora',
            aprovado=True,
        )

        self.contrato.refresh_from_db()
        self.assertEqual(self.contrato.status, StatusContrato.APROVADO_FINAL)

    def test_pendencia_resolvida_deixa_de_impactar_resultado(self):
        analise = AnaliseContrato.objects.create(contrato=self.contrato)
        pendencia = Pendencia.objects.create(
            analise=analise,
            codigo_regra='SEGURO',
            severidade=SeveridadePendencia.ERRO,
            mensagem='Seguro ausente.',
        )
        analise.recalcular_resultado()
        relatorio = analise.relatorio
        self.assertEqual(analise.resultado, ResultadoAnalise.REPROVADO)
        self.assertEqual(relatorio.status, ResultadoAnalise.REPROVADO)

        pendencia.resolvida = True
        pendencia.save()
        analise.refresh_from_db()
        self.contrato.refresh_from_db()
        relatorio.refresh_from_db()

        self.assertEqual(analise.resultado, ResultadoAnalise.APROVADO)
        self.assertEqual(self.contrato.status, StatusContrato.VALIDADO_OK)
        self.assertEqual(relatorio.status, ResultadoAnalise.APROVADO)
        self.assertIn('Resultado: APROVADO', relatorio.conteudo)

    def test_usuario_comum_so_altera_resolvida_em_pendencia_propria(self):
        analise = AnaliseContrato.objects.create(contrato=self.contrato)
        pendencia = Pendencia.objects.create(
            analise=analise,
            codigo_regra='SEGURO',
            severidade=SeveridadePendencia.PENDENCIA,
            mensagem='Revisar seguro.',
        )
        self.client.force_authenticate(user=self.auth_user)

        response = self.client.patch(
            f'/api/pendencias/{pendencia.id}/',
            {'resolvida': True},
            format='json',
        )

        pendencia.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(pendencia.resolvida)

    def test_usuario_comum_nao_altera_campos_restritos_de_pendencia(self):
        analise = AnaliseContrato.objects.create(contrato=self.contrato)
        pendencia = Pendencia.objects.create(
            analise=analise,
            codigo_regra='SEGURO',
            severidade=SeveridadePendencia.PENDENCIA,
            mensagem='Revisar seguro.',
        )
        self.client.force_authenticate(user=self.auth_user)

        response = self.client.patch(
            f'/api/pendencias/{pendencia.id}/',
            {
                'mensagem': 'Alterada',
                'severidade': SeveridadePendencia.ERRO,
                'codigo_regra': 'OUTRA',
                'analise': analise.id,
            },
            format='json',
        )

        pendencia.refresh_from_db()
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.data)
        self.assertEqual(pendencia.mensagem, 'Revisar seguro.')
        self.assertEqual(pendencia.severidade, SeveridadePendencia.PENDENCIA)

    def test_usuario_comum_nao_altera_pendencia_de_outro_usuario(self):
        analise = AnaliseContrato.objects.create(contrato=self.outro_contrato)
        pendencia = Pendencia.objects.create(
            analise=analise,
            codigo_regra='SEGURO',
            severidade=SeveridadePendencia.PENDENCIA,
            mensagem='Revisar seguro.',
        )
        self.client.force_authenticate(user=self.auth_user)

        response = self.client.patch(
            f'/api/pendencias/{pendencia.id}/',
            {'resolvida': True},
            format='json',
        )

        self.assertEqual(response.status_code, 404)

    def test_registro_cria_user_e_usuario_vinculado(self):
        response = self.client.post(
            '/api/auth/register/',
            {
                'username': 'carol',
                'email': 'carol@example.com',
                'password': 'senha123',
                'cpf': '111.222.333-44',
                'nome': 'Carol Teste',
            },
            format='json',
        )

        self.assertEqual(response.status_code, 201)
        user = AuthUser.objects.get(username='carol')
        self.assertEqual(response.data['perfil']['id'], user.perfil.id)
        self.assertEqual(response.data['perfil']['cpf'], '111.222.333-44')
        self.assertEqual(user.perfil.nome, 'Carol Teste')
        self.assertEqual(user.perfil.cpf, '111.222.333-44')

    def test_registro_rejeita_email_duplicado(self):
        response = self.client.post(
            '/api/auth/register/',
            {
                'username': 'emailduplicado',
                'email': 'alice@example.com',
                'password': 'senha123',
                'cpf': '333.444.555-66',
                'nome': 'Email Duplicado',
            },
            format='json',
        )

        self.assertEqual(response.status_code, 400)

    def test_registro_rejeita_cpf_duplicado(self):
        response = self.client.post(
            '/api/auth/register/',
            {
                'username': 'cpfduplicado',
                'email': 'cpfduplicado@example.com',
                'password': 'senha123',
                'cpf': '123.456.789-01',
                'nome': 'CPF Duplicado',
            },
            format='json',
        )

        self.assertEqual(response.status_code, 400)

    def test_registro_rejeita_campos_obrigatorios_vazios(self):
        response = self.client.post(
            '/api/auth/register/',
            {
                'username': '',
                'email': '',
                'password': '',
                'cpf': '',
                'nome': '',
            },
            format='json',
        )

        self.assertEqual(response.status_code, 400)

    def test_endpoint_me_retorna_perfil_para_usuario_recadastrado(self):
        self.client.post(
            '/api/auth/register/',
            {
                'username': 'dora',
                'email': 'dora@example.com',
                'password': 'senha123',
                'cpf': '222.333.444-55',
                'nome': 'Dora Teste',
            },
            format='json',
        )
        user = AuthUser.objects.get(username='dora')
        self.client.force_authenticate(user=user)

        response = self.client.get('/api/me/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['perfil']['cpf'], '222.333.444-55')

    def test_contrato_aprovado_final_nao_pode_ser_reanalisado_sem_reenvio(self):
        AnaliseContrato.gerar_para_contrato(self.contrato, dados_extraidos={})
        ParecerInstitucional.objects.create(
            contrato=self.contrato,
            instituicao=self.instituicao,
            autor='Maria Coordenadora',
            aprovado=True,
        )
        self.client.force_authenticate(user=self.auth_user)

        response = self.client.post(f'/api/contratos/{self.contrato.id}/analisar/', format='json')

        self.assertEqual(response.status_code, 400)

    def test_reanalise_em_status_permitido_nao_quebra_fluxo(self):
        AnaliseContrato.gerar_para_contrato(self.contrato, dados_extraidos={})
        self.contrato.refresh_from_db()
        self.assertEqual(self.contrato.status, StatusContrato.VALIDADO_OK)
        self.client.force_authenticate(user=self.auth_user)

        response = self.client.post(
            f'/api/contratos/{self.contrato.id}/analisar/',
            {'dados_extraidos': {}},
            format='json',
        )

        self.contrato.refresh_from_db()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.contrato.status, StatusContrato.VALIDADO_OK)

    def test_fluxo_principal_via_api(self):
        register_response = self.client.post(
            '/api/auth/register/',
            {
                'username': 'fluxo',
                'email': 'fluxo@example.com',
                'password': 'senha123',
                'cpf': '444.555.666-77',
                'nome': 'Usuario Fluxo',
            },
            format='json',
        )
        self.assertEqual(register_response.status_code, 201)

        login_response = self.client.post(
            '/api/auth/login/',
            {'username': 'fluxo', 'password': 'senha123'},
            format='json',
        )
        self.assertEqual(login_response.status_code, 200)
        user = AuthUser.objects.get(username='fluxo')
        perfil = user.perfil

        estagio_response = self.client.post(
            '/api/estagios/',
            {
                'empresa': self.empresa.id,
                'instituicao': self.instituicao.id,
                'curso': 'Direito',
                'tipo_estagio': TipoEstagio.OBRIGATORIO,
                'data_inicio': '2026-01-01',
                'data_fim': '2026-12-31',
                'carga_horaria_diaria': '6.00',
                'carga_horaria_semanal': '30.00',
                'atividades': 'Desenvolvimento acompanhado de sistemas internos.',
                'supervisor_nome': 'Carlos Supervisor',
                'professor_orientador': 'Ana Orientadora',
                'seguro_apolice': 'APOLICE-123',
            },
            format='json',
        )
        self.assertEqual(estagio_response.status_code, 201)

        contrato_response = self.client.post(
            '/api/contratos/',
            {
                'empresa': self.empresa.id,
                'instituicao': self.instituicao.id,
                'estagio': estagio_response.data['id'],
            },
            format='json',
        )
        self.assertEqual(contrato_response.status_code, 201)
        contrato_id = contrato_response.data['id']
        contrato = Contrato.objects.get(id=contrato_id)
        self.assertEqual(contrato.usuario, perfil)

        upload_response = self.client.post(
            f'/api/contratos/{contrato_id}/upload-pdf/',
            {'arquivo_pdf': self.pdf_upload('fluxo.pdf')},
            format='multipart',
        )
        self.assertEqual(upload_response.status_code, 200)
        self.assertEqual(upload_response.data['versao'], 1)
        self.assertEqual(VersaoContrato.objects.filter(contrato_id=contrato_id).count(), 1)

        analise_response = self.client.post(f'/api/contratos/{contrato_id}/analisar/', format='json')
        self.assertEqual(analise_response.status_code, 201)
        analise_id = analise_response.data['id']

        pendencias_response = self.client.get('/api/pendencias/', {'analise': analise_id})
        self.assertEqual(pendencias_response.status_code, 200)
        self.assertGreaterEqual(len(pendencias_response.data), 1)

        pendencia_id = pendencias_response.data[0]['id']
        resolver_response = self.client.patch(
            f'/api/pendencias/{pendencia_id}/',
            {'resolvida': True},
            format='json',
        )
        self.assertEqual(resolver_response.status_code, 200)

        relatorios_response = self.client.get('/api/relatorios/', {'analise': analise_id})
        self.assertEqual(relatorios_response.status_code, 200)
        self.assertEqual(len(relatorios_response.data), 1)

        self.client.force_authenticate(user=self.admin)
        contrato.refresh_from_db()
        if contrato.status == StatusContrato.INVALIDO_PENDENTE:
            for pendencia in contrato.analises.get(id=analise_id).pendencias.filter(resolvida=False):
                pendencia.resolvida = True
                pendencia.save()
            contrato.refresh_from_db()
        parecer_response = self.client.post(
            '/api/pareceres/',
            {
                'contrato': contrato_id,
                'instituicao': self.instituicao.id,
                'autor': 'Maria Coordenadora',
                'aprovado': True,
            },
            format='json',
        )
        self.assertEqual(parecer_response.status_code, 201)
        contrato.refresh_from_db()
        self.assertEqual(contrato.status, StatusContrato.APROVADO_FINAL)

    def test_endpoint_me(self):
        self.client.force_authenticate(user=self.auth_user)

        response = self.client.get('/api/me/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], 'alice')
        self.assertEqual(response.data['perfil']['id'], self.usuario.id)

    def test_endpoint_dashboard(self):
        self.client.force_authenticate(user=self.auth_user)
        self.contrato.status = StatusContrato.INVALIDO_PENDENTE
        self.contrato.score_conformidade = 80.0
        self.contrato.save(update_fields=['status', 'score_conformidade'])

        response = self.client.get('/api/dashboard/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['total_contratos'], 1)
        self.assertEqual(response.data['contratos_pendentes'], 1)
        self.assertEqual(response.data['media_score_conformidade'], 80.0)
