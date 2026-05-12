# app/api_urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.api import UsuarioViewSet, EmpresaViewSet, InstituicaoViewSet, ContratoViewSet, SistemaValidadorViewSet

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'empresas', EmpresaViewSet, basename='empresa')
router.register(r'instituicoes', InstituicaoViewSet, basename='instituicao')
router.register(r'contratos', ContratoViewSet, basename='contrato')
router.register(r'sistemas-validadores', SistemaValidadorViewSet, basename='sistema-validador')

urlpatterns = [
    path('', include(router.urls)),
]