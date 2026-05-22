# Projeto Back-End

**Grupo**: Pedro Santos, Gabriel Melo, Bernardo Brandao, Iago Viana, Gabriel Maccachero

## Sobre

O VerificaEstagio e uma API Django para cadastro e verificacao de contratos de estagio. O sistema registra alunos, empresas, instituicoes, estagios, contratos, analises, pendencias, relatorios de conformidade e pareceres institucionais.

## Tecnologias

- Python
- Django
- Django REST Framework
- drf-spectacular
- SQLite
- MkDocs

## Como Rodar

```powershell
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Endpoints Principais

- `GET /api/docs/`: Swagger UI
- `GET /api/redoc/`: ReDoc
- `GET /api/schema/`: schema OpenAPI
- `POST /api/auth/register/`: cadastro de usuario Django
- `POST /api/auth/login/`: login por sessao
- `POST /api/auth/logout/`: logout
- `/api/usuarios/`
- `/api/empresas/`
- `/api/instituicoes/`
- `/api/estagios/`
- `/api/contratos/`
- `/api/contratos/{id}/upload-pdf/`
- `/api/contratos/{id}/analisar/`
- `/api/analises/`
- `/api/pendencias/`
- `/api/relatorios/`
- `/api/pareceres/`

## Filtros

Alguns endpoints aceitam filtros via query string:

```text
/api/contratos/?status=RECEBIDO
/api/contratos/?usuario=1&empresa=2
/api/contratos/?data_inicio=2026-01-01&data_fim=2026-12-31
/api/estagios/?tipo_estagio=OBRIGATORIO&curso=Direito
/api/pendencias/?severidade=ERRO&resolvida=false
```

## Testes

```powershell
python manage.py check
python manage.py test
```
