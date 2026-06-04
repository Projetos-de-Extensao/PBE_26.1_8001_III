---
id: diagrama_de_sequencia
title: Diagrama de Sequência
---

## Fluxo de execução do contrato

### Visão geral
Este diagrama descreve o fluxo atual implementado no backend VerificaEstagio: autenticação, cadastro de estágio, submissão de contrato, upload de PDF, análise automática e emissão de parecer institucional.

### Diagrama de sequência

```plantuml
@startuml
actor "Usuário / Empresa" as User
participant "API VerificaEstagio" as API
participant "Estágio" as EstagioModel
participant "Contrato" as ContratoModel
participant "AnaliseContrato" as AnaliseModel
participant "ParecerInstitucional" as ParecerModel

User -> API : POST /api/auth/login/
API -> User : 200 OK

User -> API : POST /api/estagios/
API -> EstagioModel : create(...)
EstagioModel --> API : estágio criado
API -> User : 201 Created

User -> API : POST /api/contratos/
API -> ContratoModel : create(status=RECEBIDO)
ContratoModel --> API : contrato criado
API -> User : 201 Created

User -> API : POST /api/contratos/{id}/upload-pdf/
API -> ContratoModel : save arquivo_pdf
ContratoModel --> API : PDF associado
API -> User : 200 OK

User -> API : POST /api/contratos/{id}/analisar/
API -> AnaliseModel : gerar_para_contrato(contrato, dados_extraidos)
AnaliseModel -> EstagioModel : validar_regras_negocio()
AnaliseModel --> ContratoModel : atualizar status e score
AnaliseModel --> API : análise criada
API -> User : 201 Created

User -> API : GET /api/analises/?contrato={id}
API -> AnaliseModel : retorna análise e pendências
API -> User : 200 OK

User -> API : POST /api/pareceres/
API -> ParecerModel : create(...)
ParecerModel --> ContratoModel : atualiza status para APROVADO_FINAL / INVALIDO_PENDENTE
API -> User : 201 Created

@enduml
```

### Observações
- A análise gera pendências a partir do estágio associado ao contrato.
- `AnaliseContrato.gerar_para_contrato()` recalcula resultado e cria o relatório de conformidade.
- O parecer institucional atualiza o status do contrato para APROVADO_FINAL quando aprovado.

