---
id: casos_de_uso
title: Casos de Uso
---

## Casos de uso principais

### 1. Cadastrar estágio
- Atores: Aluno, Empresa, Instituição
- Descrição: o estágio é registrado com dados de curso, carga horária, supervisor, professor orientador e seguro.
- Resultado esperado: estágio existente no sistema e pronto para associação ao contrato.

### 2. Submeter contrato
- Atores: Aluno, Empresa
- Descrição: o contrato é criado e vinculado ao estágio e à instituição.
- Resultado esperado: contrato com status RECEBIDO disponível na API.

### 3. Upload de contrato em PDF
- Atores: Aluno, Empresa
- Descrição: o arquivo PDF do contrato é enviado ao sistema.
- Resultado esperado: arquivo aceito apenas se for PDF e vinculado ao contrato.

### 4. Analisar contrato
- Atores: Sistema
- Descrição: o backend executa validações de regras de estágio, gera pendências e atualiza o status do contrato.
- Resultado esperado: análise criada com resultado APROVADO, PENDENTE ou REPROVADO.

### 5. Consultar pendências e relatórios
- Atores: Aluno, Empresa, Instituição
- Descrição: os resultados da análise são disponibilizados com pendências detalhadas e relatório de conformidade.
- Resultado esperado: pendências listadas e relatório associadas à análise.

### 6. Emitir parecer institucional
- Atores: Instituição de ensino
- Descrição: a instituição registra um parecer final sobre o contrato.
- Resultado esperado: contrato recebe status APROVADO_FINAL ou INVALIDO_PENDENTE.

## Diagrama de casos de uso

```plantuml
@startuml
left to right direction
skinparam packageStyle rectangle

actor "Aluno / Usuário" as Usuario
actor "Empresa" as Empresa
actor "Instituição de Ensino" as Instituicao

package "VerificaEstagio" {
    usecase "Cadastrar Estágio" as U1
    usecase "Criar Contrato" as U2
    usecase "Upload de PDF" as U3
    usecase "Analisar Contrato" as U4
    usecase "Consultar Pendências" as U5
    usecase "Gerar Relatório" as U6
    usecase "Emitir Parecer" as U7
}

Usuario --> U1
Usuario --> U2
Usuario --> U3

Empresa --> U2
Empresa --> U3

U2 ..> U4 : <<include>>
U3 ..> U4 : <<include>>
U4 --> U5
U4 --> U6

Instituicao --> U5
Instituicao --> U6
Instituicao --> U7
U7 ..> U2 : <<extend>>

@enduml
```

## Alinhamento com o backend atual
- Endpoints disponíveis: `/api/estagios/`, `/api/contratos/`, `/api/analises/`, `/api/pendencias/`, `/api/relatorios/`, `/api/pareceres/`.
- Autenticação: registro, login e logout via sessão.
- O sistema atual não implementa interface gráfica nem envio automático de notificações.

