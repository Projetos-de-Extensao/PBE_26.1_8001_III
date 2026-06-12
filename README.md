# VerificaEstagio API

**Grupo**: Pedro Santos, Gabriel Melo, Bernardo Brandao, Iago Viana, Gabriel Maccachero

## Objetivo

O VerificaEstagio e uma API Django REST para cadastro, upload, analise e validacao de contratos de estagio. A primeira etapa entrega o backend base para:

- cadastro de usuarios e perfil de dominio;
- cadastro de empresas, instituicoes, estagios e contratos;
- upload e versionamento de PDFs de contrato;
- extracao simples de dados de PDF com `pdfplumber`;
- analise automatica, pendencias e relatorio de conformidade;
- parecer institucional final;
- isolamento de dados por usuario autenticado.

## Tecnologias

- Python 3
- Django
- Django REST Framework
- drf-spectacular para Swagger/OpenAPI
- django-cors-headers
- pdfplumber
- SQLite em desenvolvimento

## Configuracao

Crie e ative um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instale as dependencias:

```powershell
python -m pip install -r requirements.txt
```

Variaveis de ambiente aceitas:

```powershell
$env:DJANGO_DEBUG="true"
$env:DJANGO_SECRET_KEY="uma-chave-segura-em-producao"
$env:DJANGO_ALLOWED_HOSTS="localhost,127.0.0.1"
$env:DJANGO_CORS_ALLOWED_ORIGINS="http://localhost:5173,http://127.0.0.1:5173"
$env:DJANGO_CSRF_TRUSTED_ORIGINS="http://localhost:5173,http://127.0.0.1:5173"
$env:CONTRATO_PDF_MAX_SIZE="10485760"
```

Em desenvolvimento, se `DJANGO_DEBUG=true` e `DJANGO_SECRET_KEY` nao existir, o projeto usa uma chave fixa apenas para dev. Em producao (`DJANGO_DEBUG=false`), `DJANGO_SECRET_KEY` e obrigatoria.

## Banco de Dados

Rode as migrations:

```powershell
python manage.py migrate
```

Opcionalmente crie um superusuario:

```powershell
python manage.py createsuperuser
```

## Executar

```powershell
python manage.py runserver
```

URLs locais:

- API: `http://127.0.0.1:8000/api/`
- Admin: `http://127.0.0.1:8000/admin/`
- Swagger: `http://127.0.0.1:8000/api/docs/`
- ReDoc: `http://127.0.0.1:8000/api/redoc/`
- OpenAPI schema: `http://127.0.0.1:8000/api/schema/`

## Testes

Antes de abrir PR, rode:

```powershell
python manage.py check
python manage.py makemigrations --check
python manage.py test
```

## Fluxo Principal

1. Registrar usuario em `POST /api/auth/register/`.
2. Autenticar em `POST /api/auth/login/`.
3. Criar estagio em `POST /api/estagios/`.
4. Criar contrato em `POST /api/contratos/`.
5. Enviar PDF em `POST /api/contratos/{id}/upload-pdf/`.
6. Analisar contrato em `POST /api/contratos/{id}/analisar/`.
7. Listar pendencias em `GET /api/pendencias/`.
8. Resolver pendencia com `PATCH /api/pendencias/{id}/` enviando apenas `{"resolvida": true}`.
9. Consultar relatorio em `GET /api/relatorios/`.
10. Staff/admin emite parecer final em `POST /api/pareceres/`.

## Endpoints Principais

| Metodo | Endpoint | Descricao | Permissao |
| --- | --- | --- | --- |
| POST | `/api/auth/register/` | Cria `User` e perfil `Usuario` | Publico |
| POST | `/api/auth/login/` | Login por sessao | Publico |
| POST | `/api/auth/logout/` | Logout | Autenticado |
| GET | `/api/me/` | Dados do usuario autenticado e perfil | Autenticado |
| GET | `/api/dashboard/` | Resumo de contratos, scores e pendencias | Autenticado |
| GET/PATCH | `/api/usuarios/` | Perfil do usuario; staff ve todos | Autenticado |
| GET | `/api/empresas/` | Empresas vinculadas ao usuario; staff ve todas | Autenticado |
| POST/PATCH/DELETE | `/api/empresas/` | Administracao de empresas | Staff/admin |
| GET | `/api/instituicoes/` | Instituicoes vinculadas ao usuario; staff ve todas | Autenticado |
| POST/PATCH/DELETE | `/api/instituicoes/` | Administracao de instituicoes | Staff/admin |
| GET/POST/PATCH/DELETE | `/api/estagios/` | Estagios do usuario autenticado | Autenticado |
| GET/POST/PATCH/DELETE | `/api/contratos/` | Contratos do usuario autenticado | Autenticado |
| POST | `/api/contratos/{id}/upload-pdf/` | Upload validado de PDF e criacao de versao | Dono do contrato ou staff |
| POST | `/api/contratos/{id}/analisar/` | Executa analise automatica do contrato | Dono do contrato ou staff |
| GET | `/api/analises/` | Lista analises; criacao direta bloqueada | Autenticado |
| GET/PATCH | `/api/pendencias/` | Lista pendencias; PATCH apenas em `resolvida` | Autenticado |
| GET | `/api/relatorios/` | Lista relatorios; criacao direta bloqueada | Autenticado |
| GET | `/api/sistemas-validadores/` | Consulta sistemas validadores; escrita direta bloqueada | Autenticado |
| GET | `/api/regras-validacao/` | Lista regras de validacao | Autenticado |
| POST/PATCH/DELETE | `/api/regras-validacao/` | Administracao de regras | Staff/admin |
| GET | `/api/pareceres/` | Lista pareceres acessiveis | Autenticado |
| POST/PATCH/DELETE | `/api/pareceres/` | Emissao e administracao de pareceres | Staff/admin |

## Regras de Seguranca

- Endpoints sensiveis exigem autenticacao.
- Usuario comum so ve dados vinculados ao proprio perfil.
- Recursos administrativos, como empresas, instituicoes, regras e pareceres, possuem escrita restrita a staff/admin.
- Analises, relatorios e sistemas validadores sao expostos como somente leitura; a analise deve ser criada pela action do contrato.
- Pendencias podem ser alteradas por usuario comum apenas no campo `resolvida`.

## Upload e Validacao de PDF

O upload de contrato aceita apenas PDFs:

- com extensao `.pdf`;
- com `content_type` compativel;
- nao vazios;
- abaixo de `CONTRATO_PDF_MAX_SIZE` bytes;
- legiveis pelo `pdfplumber`;
- com texto extraivel.

Cada upload valido cria uma nova `VersaoContrato` com copia propria do arquivo enviado. Upload invalido nao incrementa versao nem altera status.

## Status da Etapa 1

Estado atual: backend da primeira etapa pronto para revisao tecnica.

Inclui modelos, serializers, endpoints protegidos, Swagger/ReDoc, upload e versionamento de PDF, analise automatica inicial, pendencias, relatorios, parecer institucional, logs simples em fluxos criticos e testes cobrindo seguranca, validacoes e fluxo principal.
