# Design Thinking

---

## 1. Infos

**Título do Projeto:** VerificaEstágio — Sistema de Verificação Contratual de Estágio  
**Equipe:** Gabriel Melo, Bernardo Brandão, Iago Viana, Pedro Dos Santos e Gabriel m 
**Data:** 19/04/2026
**Instituição:** IBMEC  

---

## 2. Introdução

### Contexto do Projeto

Atualmente, a análise de contratos de estágio é realizada de forma manual por instituições de ensino, o que torna o processo lento, suscetível a erros e inconsistências. Além disso, a verificação exige conhecimento da legislação (Lei nº 11.788/2008) e atenção a diversos detalhes contratuais.

### Objetivo

Desenvolver um sistema capaz de automatizar a verificação de contratos de estágio, identificando inconsistências, ausência de cláusulas obrigatórias e possíveis irregularidades legais.

### Público-Alvo

- Estudantes
- Empresas
- Instituições de ensino
- Setores de estágio

### Escopo

O sistema irá:
- Receber contratos em PDF
- Extrair informações automaticamente
- Validar regras legais e institucionais
- Gerar relatórios de conformidade

Não está no escopo:
- Substituir completamente a validação humana
- Criar contratos automaticamente (fase futura)

---

## 3. Fases do Design Thinking

---

### 3.1 Empatia

#### Pesquisa

Foram utilizados os seguintes métodos:

- Observação do processo atual de análise de contratos
- Análise de requisitos legais (Lei do Estágio)
- Discussões em grupo (brainstorm)
- Experiência dos próprios alunos com estágio

#### Insights

- O processo manual é demorado
- Há risco de erro humano
- Nem todos conhecem a legislação corretamente
- Falta padronização na análise
- A validação pode variar de pessoa para pessoa

#### Personas

**Persona 1 — Estudante**
- Nome: João
- Idade: 20 anos
- Problema: demora na aprovação do estágio

**Persona 2 — Coordenador**
- Nome: Maria
- Idade: 45 anos
- Problema: excesso de contratos para analisar

**Persona 3 — Empresa**
- Nome: TechCorp
- Problema: atrasos na validação prejudicam início do estágio

---

### 3.2 Definição

#### Problema Central

> Como podemos automatizar a verificação de contratos de estágio para reduzir erros, tempo de análise e riscos legais?

#### Pontos de Vista (POV)

- O estudante precisa de rapidez na aprovação para iniciar o estágio
- A instituição precisa de precisão na validação
- A empresa precisa de agilidade no processo

---

### 3.3 Ideação

#### Brainstorming

- Sistema de leitura automática de contratos
- Validação baseada em regras legais
- Geração de relatório automático
- Interface simples para envio de contratos
- Dashboard para acompanhamento

#### Seleção de Ideias

Critérios utilizados:
- Viabilidade técnica
- Impacto no problema
- Facilidade de implementação

#### Ideias Selecionadas

- Sistema de upload de contrato
- Motor de validação automática
- Relatório de conformidade
- Painel administrativo

---

### 3.4 Prototipagem

#### Descrição do Protótipo

Foi desenvolvido um protótipo digital contendo:

- Tela de login
- Tela de upload de contrato
- Tela de resultado da análise
- Relatório detalhado

#### Materiais Utilizados

- MkDocs (documentação)
- Protótipos em interface digital
- Modelagem conceitual (diagramas)

#### Testes Realizados

- Simulação de envio de contratos
- Testes com diferentes cenários:
  - contrato completo
  - contrato incompleto
  - contrato irregular

---

### 3.5 Teste

#### Feedback dos Usuários

- Interface simples e intuitiva
- Redução significativa do tempo de análise
- Necessidade de validação humana em alguns casos

#### Ajustes Realizados

- Melhorias na clareza dos relatórios
- Inclusão de alertas mais detalhados
- Melhor organização das informações

#### Resultados Finais

O sistema conseguiu:
- Identificar inconsistências automaticamente
- Reduzir o tempo de análise
- Padronizar o processo de validação

---

## 4. Conclusão

### Resultados Obtidos

- Automação parcial do processo de análise
- Redução de erros humanos
- Maior padronização

### Próximos Passos

- Implementação completa do sistema
- Integração com bases institucionais
- Uso de IA para análise semântica mais avançada

### Aprendizados

- Importância da empatia com o usuário
- Necessidade de equilíbrio entre automação e validação humana
- Valor de processos iterativos

---

## 5. Anexos

- Mapas mentais
- Diagramas UML
- Protótipos de interface
- Documentos de requisitos