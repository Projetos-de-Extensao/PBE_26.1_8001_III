# Levantamento de Requisitos e Caso de Uso

**Sistema:** VerificaEstágio — Sistema de Verificação Contratual de Estágio

---

## 1. Identificação dos Stakeholders

- **Aluno / Estagiário:** usuário que submete ou acompanha a análise do contrato de estágio.
- **Empresa / Parte concedente:** responsável por cadastrar a vaga, enviar o contrato e acompanhar pendências.
- **Instituição de ensino:** valida conformidade acadêmica e institucional do estágio.
- **Coordenador / Setor de Estágios:** revisa contratos com pendências, aprova, reprova ou solicita ajustes.
- **Supervisor da empresa:** pessoa indicada no contrato para acompanhar o estagiário.
- **Administrador do sistema:** gerencia usuários, parâmetros legais, regras de validação e relatórios.

---

## 2. Requisitos Funcionais

| ID   | Descrição | Prioridade |
|------|-----------|------------|
| RF01 | O sistema deve permitir cadastro e autenticação de usuários por perfil (aluno, empresa, instituição e administrador). | Alta |
| RF02 | O sistema deve permitir o upload do contrato de estágio em PDF. | Alta |
| RF03 | O sistema deve extrair informações relevantes do contrato, como nome do aluno, empresa, instituição, carga horária, vigência, supervisor, seguro e atividades. | Alta |
| RF04 | O sistema deve verificar se o contrato contém os elementos mínimos exigidos pela Lei do Estágio. | Alta |
| RF05 | O sistema deve comparar a carga horária informada com os limites legais aplicáveis ao tipo de estágio e nível de ensino. | Alta |
| RF06 | O sistema deve verificar se há indicação de supervisor da parte concedente. | Alta |
| RF07 | O sistema deve verificar se há informação sobre seguro contra acidentes pessoais, quando exigido. | Alta |
| RF08 | O sistema deve verificar se as atividades descritas são compatíveis com a formação do estudante e com o caráter educativo do estágio. | Alta |
| RF09 | O sistema deve apontar cláusulas ausentes, inconsistentes ou potencialmente irregulares. | Alta |
| RF10 | O sistema deve gerar um relatório automático de conformidade com status: aprovado, pendente ou reprovado. | Alta |
| RF11 | O sistema deve permitir que a instituição registre parecer manual complementar. | Média |
| RF12 | O sistema deve armazenar histórico de análises e versões de documentos. | Média |
| RF13 | O sistema deve notificar os responsáveis quando houver pendências ou necessidade de reenviar documentos. | Média |
| RF14 | O sistema deve permitir consulta de contratos e relatórios por filtros, como aluno, empresa, status e período. | Média |
| RF15 | O sistema deve disponibilizar painel administrativo com métricas de análises realizadas, pendências e irregularidades mais comuns. | Baixa |

---

## 3. Requisitos Não Funcionais

- **RNF01 – Desempenho:** o sistema deve processar e gerar a análise inicial do contrato em tempo adequado para uso institucional.
- **RNF02 – Segurança:** os documentos e dados pessoais devem ser protegidos com autenticação, controle de acesso por perfil e armazenamento seguro.
- **RNF03 – Usabilidade:** a interface deve ser simples, com fluxo claro de envio, análise e retorno.
- **RNF04 – Confiabilidade:** as regras de validação devem ser rastreáveis e baseadas na legislação e nas normas institucionais.
- **RNF05 – Auditabilidade:** o sistema deve registrar data, usuário, versão do contrato e resultado da análise.
- **RNF06 – Escalabilidade:** o sistema deve suportar múltiplos contratos e múltiplos usuários simultaneamente.
- **RNF07 – Manutenibilidade:** as regras legais devem poder ser atualizadas sem reescrever todo o sistema.
- **RNF08 – Compatibilidade:** o sistema deve aceitar contratos em formato PDF.
- **RNF09 – Transparência:** o relatório deve explicar claramente por que um contrato foi aprovado, pendente ou reprovado.

Esses requisitos se conectam diretamente às obrigações legais do estágio, que envolvem termo de compromisso, compatibilidade educacional, supervisão, jornada e acompanhamento institucional.

---

## 4. Exemplo de Caso de Uso

### UC01 - Verificar Contrato de Estágio

**Atores:** Aluno, Empresa, Sistema, Instituição de Ensino.

**Pré-condição:** usuário autenticado e contrato em formato aceito pelo sistema.

#### Fluxo Principal

1. O usuário realiza upload do contrato.
2. O sistema identifica e extrai os dados principais do documento.
3. O sistema aplica as regras de validação jurídica e institucional.
4. O sistema verifica presença de cláusulas obrigatórias.
5. O sistema compara carga horária, vigência e informações do supervisor.
6. O sistema verifica a existência de informações sobre seguro.
7. O sistema analisa a descrição das atividades.
8. O sistema gera relatório de conformidade.
9. A instituição consulta o relatório e registra o parecer final, se necessário.

#### Fluxos Alternativos

- **FA1:** documento ilegível ou corrompido → sistema rejeita o arquivo e solicita novo envio.
- **FA2:** ausência de cláusulas obrigatórias → sistema marca o contrato como pendente ou irregular.
- **FA3:** carga horária acima do permitido → sistema sinaliza inconformidade legal.
- **FA4:** atividades incompatíveis com o curso → sistema sinaliza análise manual obrigatória.
- **FA5:** ausência de supervisor ou seguro → sistema aponta pendência documental.

**Pós-condição:** contrato classificado como aprovado, pendente ou reprovado, com relatório armazenado no sistema.

---

## 5. Protótipo (Exemplo Simplificado)

- **Tela de Login:** acesso por perfil.
- **Tela de Upload de Contrato:** envio do PDF + identificação do aluno/empresa.
- **Tela de Resultado da Análise:** resumo com conformidades e inconformidades.
- **Tela de Relatório Detalhado:** lista de critérios avaliados, justificativas e observações.
- **Tela de Revisão Institucional:** campo para parecer do coordenador ou setor de estágio.
- **Painel Administrativo:** métricas gerais, filtros e histórico.

---

## 6. Validação

- Validar com o setor de estágios se as regras automáticas refletem o fluxo real de conferência documental.
- Validar com professores/coordenadores se a análise das atividades está compatível com o projeto pedagógico.
- Realizar testes com contratos válidos e contratos com falhas propositalmente inseridas.
- Comparar o resultado do sistema com a análise manual de um responsável institucional.
- Verificar se os critérios usados no sistema correspondem às exigências da Lei nº 11.788/2008 e às normas internas da instituição.

---

# Diagrama de Casos de Uso

## Código PlantUML

```plantuml
@startuml VerificaEstagio_CasosDeUso

left to right direction
skinparam actorStyle awesome

actor Aluno
actor Empresa
actor "Instituição de Ensino" as Instituicao
actor Administrador

usecase (UC01: Enviar Contrato) as UC01
usecase (UC02: Extrair Dados do Contrato) as UC02
usecase (UC03: Validar Cláusulas Obrigatórias) as UC03
usecase (UC04: Verificar Jornada) as UC04
usecase (UC05: Verificar Supervisor e Seguro) as UC05
usecase (UC06: Avaliar Atividades do Estágio) as UC06
usecase (UC07: Gerar Relatório de Conformidade) as UC07
usecase (UC08: Emitir Parecer Institucional) as UC08
usecase (UC09: Gerenciar Regras do Sistema) as UC09

usecase (FA1: Documento Ilegível) as FA1
usecase (FA2: Cláusulas Ausentes) as FA2
usecase (FA3: Carga Horária Irregular) as FA3
usecase (FA4: Atividades Incompatíveis) as FA4

Aluno --> UC01
Empresa --> UC01
Instituicao --> UC08
Administrador --> UC09

UC01 --> UC02 : <<include>>
UC02 --> UC03 : <<include>>
UC03 --> UC04 : <<include>>
UC04 --> UC05 : <<include>>
UC05 --> UC06 : <<include>>
UC06 --> UC07 : <<include>>
UC07 --> UC08 : <<extend>>

FA1 .> UC02 : <<extend>>
FA2 .> UC03 : <<extend>>
FA3 .> UC04 : <<extend>>
FA4 .> UC06 : <<extend>>

note right of UC07
  Pré-condição: contrato enviado.
  Pós-condição: relatório gerado com
  status aprovado, pendente ou reprovado.
end note

@enduml