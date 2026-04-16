---
id: diagrama_de_casos de uso
title: Diagrama de Casos de Uso
---

## Casos de Uso

### Diagrama:
@startuml
left to right direction
skinparam packageStyle rectangle

' Atores
actor "Empresa" as Empresa
actor "Aluno / Usuário" as Aluno
actor "Instituição de Ensino" as Instituicao

' Sistema e Casos de Uso
package "Sistema de Validação de Contratos" {
    
    usecase "Submeter Contrato" as UC01
    usecase "Extrair Informações" as UC02
    usecase "Calcular % de Validação" as UC03
    usecase "Notificar Pendências / Solicitar Novo" as UC04
    usecase "Encaminhar para Instituição" as UC05
    usecase "Analisar Contrato Validado" as UC06
    usecase "Aprovar Estágio" as UC07
}

' Relacionamentos de Submissão
Empresa --> UC01 : "Envia direto"
Aluno --> UC01 : "Faz upload"

' Fluxo Automático do Sistema (Includes)
UC01 ..> UC02 : <<include>>
UC02 ..> UC03 : <<include>>

' Fluxos Condicionais (Extends baseados na Porcentagem)
UC03 <.. UC04 : <<extend>> \n(Se Invalido/Com erros)
UC03 <.. UC05 : <<extend>> \n(Se Válido/Aprovável)

' Ações da Instituição
Instituicao --> UC06
UC05 ..> UC06 : <<include>>
Instituicao --> UC07 : "Aprovação Final"
UC06 ..> UC07 : <<extend>>

' Notificações de retorno
UC04 --> Empresa : "Aviso de erro"
UC04 --> Aluno : "Aviso de erro"

@enduml
