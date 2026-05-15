import os
import django
from django.db import transaction

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

django.setup()

from app.models import Usuario, Empresa, Instituicao, Contrato, SistemaValidador, StatusContrato


def create_usuarios():
    exemplos = [
        {'cpf': '123.456.789-01', 'nome': 'Alice Santos', 'email': 'alice.santos@example.com'},
        {'cpf': '234.567.890-12', 'nome': 'Bruno Alves', 'email': 'bruno.alves@example.com'},
        {'cpf': '345.678.901-23', 'nome': 'Carla Pereira', 'email': 'carla.pereira@example.com'},
        {'cpf': '456.789.012-34', 'nome': 'Diego Costa', 'email': 'diego.costa@example.com'},
        {'cpf': '567.890.123-45', 'nome': 'Elisa Rodrigues', 'email': 'elisa.rodrigues@example.com'},
    ]
    usuarios = []
    for dados in exemplos:
        usuario, _ = Usuario.objects.get_or_create(cpf=dados['cpf'], defaults=dados)
        usuarios.append(usuario)
    return usuarios


def create_empresas():
    exemplos = [
        {'cnpj': '12.345.678/0001-91', 'razao_social': 'TechNova S.A.', 'responsavel': 'Marcos Lima'},
        {'cnpj': '23.456.789/0001-02', 'razao_social': 'GreenLog Comércio Ltda.', 'responsavel': 'Fernanda Moraes'},
        {'cnpj': '34.567.890/0001-13', 'razao_social': 'InovaEdu Tecnologia', 'responsavel': 'Ricardo Menezes'},
        {'cnpj': '45.678.901/0001-24', 'razao_social': 'Construtec Engenharia', 'responsavel': 'Patrícia Souza'},
        {'cnpj': '56.789.012/0001-35', 'razao_social': 'SaúdeMais Serviços', 'responsavel': 'Júlio Ferreira'},
    ]
    empresas = []
    for dados in exemplos:
        empresa, _ = Empresa.objects.get_or_create(cnpj=dados['cnpj'], defaults=dados)
        empresas.append(empresa)
    return empresas


def create_instituicoes():
    exemplos = [
        {'nome_unidade': 'Instituto de Pesquisa do Norte', 'coordenador': 'Ana Beatriz'},
        {'nome_unidade': 'Centro de Estudos Sul', 'coordenador': 'Carlos Henrique'},
        {'nome_unidade': 'Laboratório de Inovação Leste', 'coordenador': 'Beatriz Dias'},
        {'nome_unidade': 'Núcleo de Gestão Oeste', 'coordenador': 'Fábio Gomes'},
        {'nome_unidade': 'Unidade de Apoio Central', 'coordenador': 'Marta Lima'},
    ]
    instituicoes = []
    for dados in exemplos:
        instituicao, _ = Instituicao.objects.get_or_create(nome_unidade=dados['nome_unidade'], defaults=dados)
        instituicoes.append(instituicao)
    return instituicoes


def create_contratos(usuarios, empresas, instituicoes):
    exemplos = [
        {
            'empresa': empresas[0],
            'usuario': usuarios[0],
            'instituicao': instituicoes[0],
            'status': StatusContrato.RECEBIDO,
            'score_conformidade': 10.0,
            'arquivo_original': 'Contrato de prestação de serviços - TechNova',
        },
        {
            'empresa': empresas[1],
            'usuario': usuarios[1],
            'instituicao': instituicoes[1],
            'status': StatusContrato.PROCESSANDO,
            'score_conformidade': 45.5,
            'arquivo_original': 'Contrato de fornecimento - GreenLog',
        },
        {
            'empresa': empresas[2],
            'usuario': usuarios[2],
            'instituicao': instituicoes[2],
            'status': StatusContrato.INVALIDO_PENDENTE,
            'score_conformidade': 22.0,
            'arquivo_original': 'Contrato educacional - InovaEdu',
        },
        {
            'empresa': empresas[3],
            'usuario': usuarios[3],
            'instituicao': instituicoes[3],
            'status': StatusContrato.VALIDADO_OK,
            'score_conformidade': 88.0,
            'arquivo_original': 'Contrato de obra - Construtec',
        },
        {
            'empresa': empresas[4],
            'usuario': usuarios[4],
            'instituicao': instituicoes[4],
            'status': StatusContrato.APROVADO_FINAL,
            'score_conformidade': 99.5,
            'arquivo_original': 'Contrato de saúde - SaúdeMais',
        },
    ]

    contratos = []
    for dados in exemplos:
        arquivo_original_bytes = dados['arquivo_original'].encode('utf-8')
        contrato, _ = Contrato.objects.get_or_create(
            empresa=dados['empresa'],
            usuario=dados['usuario'],
            arquivo_original=arquivo_original_bytes,
            defaults={
                'instituicao': dados['instituicao'],
                'status': dados['status'],
                'score_conformidade': dados['score_conformidade'],
            },
        )
        contrato.instituicao = dados['instituicao']
        contrato.status = dados['status']
        contrato.score_conformidade = dados['score_conformidade']
        contrato.arquivo_original = arquivo_original_bytes
        contrato.save()
        contratos.append(contrato)
    return contratos


def create_sistemas_validadores(contratos):
    sistemas = []
    for contrato in contratos:
        sistema, _ = SistemaValidador.objects.get_or_create(contrato=contrato)
        sistemas.append(sistema)
    return sistemas


if __name__ == '__main__':
    with transaction.atomic():
        usuarios = create_usuarios()
        empresas = create_empresas()
        instituicoes = create_instituicoes()
        contratos = create_contratos(usuarios, empresas, instituicoes)
        sistemas = create_sistemas_validadores(contratos)

    print(f'Criados {len(usuarios)} Usuários, {len(empresas)} Empresas, {len(instituicoes)} Instituições, {len(contratos)} Contratos e {len(sistemas)} Sistemas Validador.')