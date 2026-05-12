# app/api.py
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from app.models import Usuario, Empresa, Instituicao, Contrato, SistemaValidador
from app.serializers import UsuarioSerializer, EmpresaSerializer, InstituicaoSerializer, ContratoSerializer, SistemaValidadorSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer

class InstituicaoViewSet(viewsets.ModelViewSet):
    queryset = Instituicao.objects.all()
    serializer_class = InstituicaoSerializer

class ContratoViewSet(viewsets.ModelViewSet):
    queryset = Contrato.objects.all()
    serializer_class = ContratoSerializer

class SistemaValidadorViewSet(viewsets.ModelViewSet):
    queryset = SistemaValidador.objects.all()
    serializer_class = SistemaValidadorSerializer