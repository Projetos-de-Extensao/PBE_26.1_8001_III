from django.contrib import admin
from .models import Usuario, Empresa, Instituicao, Contrato, SistemaValidador

admin.site.register(Usuario)
admin.site.register(Empresa)
admin.site.register(Instituicao)
admin.site.register(Contrato)
admin.site.register(SistemaValidador)
