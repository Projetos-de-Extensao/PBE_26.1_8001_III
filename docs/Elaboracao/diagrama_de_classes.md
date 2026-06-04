---
id: diagrama_de_classes
title: Diagrama de Classes
---

## Diagrama de classes

### Diagrama:

```plantuml
@startuml
skinparam classAttributeIconSize 0
left to right direction

class Usuario {
  - cpf: String
  - nome: String
  - email: String
  + __str__(): String
}

class Empresa {
  - cnpj: String
  - razao_social: String
  - responsavel: String
  + __str__(): String
}

class Instituicao {
  - nome_unidade: String
  - coordenador: String
  + analisar_contrato(contrato): void
  + emitir_parecer_final(contrato, aprovado: Boolean): void
}

class Estagio {
  - usuario: Usuario
  - empresa: Empresa
  - instituicao: Instituicao
  - curso: String
  - nivel_ensino: NivelEnsino
  - tipo_estagio: TipoEstagio
  - data_inicio: Date
  - data_fim: Date
  - carga_horaria_diaria: Decimal
  - carga_horaria_semanal: Decimal
  - atividades: Text
  - supervisor_nome: String
  - professor_orientador: String
  - seguro_apolice: String
  - bolsa_auxilio: Decimal
  - auxilio_transporte: Boolean
  - plano_atividades: Text
  + validar_regras_negocio(): List
  + status_validacao(): ResultadoAnalise
}

class Contrato {
  - empresa: Empresa
  - usuario: Usuario
  - instituicao: Instituicao
  - estagio: Estagio
  - data_submissao: DateTime
  - versao: Integer
  - arquivo_original: Binary
  - arquivo_pdf: File
  - status: StatusContrato
  - score_conformidade: Float
  + atualizar_status(novo_status: StatusContrato): void
}

class AnaliseContrato {
  - contrato: Contrato
  - resultado: ResultadoAnalise
  - score_conformidade: Float
  - dados_extraidos: JSON
  - observacoes: Text
  + gerar_para_contrato(contrato, dados_extraidos): AnaliseContrato
  + recalcular_resultado(): void
  + resumo_textual(): String
}

class Pendencia {
  - analise: AnaliseContrato
  - regra: RegraValidacao
  - codigo_regra: String
  - severidade: SeveridadePendencia
  - mensagem: Text
  - resolvida: Boolean
}

class RelatorioConformidade {
  - analise: AnaliseContrato
  - status: ResultadoAnalise
  - conteudo: Text
}

class ParecerInstitucional {
  - contrato: Contrato
  - instituicao: Instituicao
  - autor: String
  - aprovado: Boolean
  - observacao: Text
}

class RegraValidacao {
  - codigo: String
  - nome: String
  - descricao: Text
  - severidade_padrao: SeveridadePendencia
  - ativa: Boolean
  + defaults(): List
  + obter_config(codigo, severidade_padrao): RegraValidacao
}

class SistemaValidador {
  - contrato: Contrato
  + extrair_dados_ocr(): Map
  + validar_regras(dados): AnaliseContrato
  + gerar_relatorio_validacao(): String
}

enum StatusContrato {
  RECEBIDO
  PROCESSANDO
  INVALIDO_PENDENTE
  VALIDADO_OK
  APROVADO_FINAL
}

enum TipoEstagio {
  OBRIGATORIO
  NAO_OBRIGATORIO
}

enum ResultadoAnalise {
  APROVADO
  PENDENTE
  REPROVADO
}

enum SeveridadePendencia {
  INFO
  PENDENCIA
  ERRO
}

Usuario "1" -- "0..*" Estagio : "cadastra"
Empresa "1" -- "0..*" Estagio : "oferece"
Instituicao "1" -- "0..*" Estagio : "acompanha"
Estagio "1" -- "0..*" Contrato : "origina"
Contrato "1" -- "0..*" AnaliseContrato : "gera"
AnaliseContrato "1" -- "0..*" Pendencia : "produz"
AnaliseContrato "1" -- "1" RelatorioConformidade : "gera"
Contrato "1" -- "0..1" ParecerInstitucional : "recebe"
Contrato "1" -- "1" SistemaValidador : "valida"
AnaliseContrato "1" -- "0..1" RegraValidacao : "referencia"

@enduml
```