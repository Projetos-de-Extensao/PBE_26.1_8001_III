# app/serializers.py
from rest_framework import serializers
from app.models import Usuario, Empresa, Instituicao, Contrato, SistemaValidador
from django.contrib.auth import authenticate

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


# --- Autenticação ---
# TESTAR AUTENTICAÇÃO
#confirmar com o jonh

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = Usuario
        fields = ['id', 'cpf', 'username', 'email', 'password']
        read_only_fields = ['id']

    def create(self, validated_data):
        password = validated_data.pop('password')
        usuario = Usuario(**validated_data)
        usuario.set_password(password)
        usuario.save()
        return usuario

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


    def validate(self, data):
        user = authenticate(**data)
        if not user:
            raise serializers.ValidationError('Credenciais inválidas.')
        return user

class SistemaValidadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = SistemaValidador
        fields = ['id', 'contrato']
        read_only_fields = ['id']


