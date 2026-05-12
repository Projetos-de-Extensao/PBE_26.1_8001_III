# app/serializers.py
from rest_framework import serializers
from app.models import Usuario, Empresa, Instituicao, Contrato, SistemaValidador

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'cpf', 'nome', 'email']
        read_only_fields = ['id']

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

class ContratoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contrato
        fields = ['id', 'empresa', 'usuario', 'instituicao', 'data_submissao', 'arquivo_original']
        read_only_fields = ['id']

class SistemaValidadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = SistemaValidador
        fields = ['id', 'contrato']
        read_only_fields = ['id']