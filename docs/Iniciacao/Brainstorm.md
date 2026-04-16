# Brainstorm do Projeto

## 1. Qual é o problema real que o sistema resolve?

Antes de pensar em tela, banco ou código, é necessário definir com clareza o problema principal.

O projeto busca resolver três dores principais:

### 1.1 Falta de padronização
Atualmente, a análise de contratos de estágio é feita de forma manual, o que gera inconsistências.

### 1.2 Risco jurídico
Um contrato pode estar em desacordo com a Lei do Estágio.

### 1.3 Risco acadêmico/institucional
Mesmo que o contrato esteja correto juridicamente, ele pode não atender às exigências da instituição.

### Pergunta central

> Como automatizar ou padronizar a verificação de contratos de estágio para reduzir erros, acelerar análises e melhorar a comunicação entre aluno, empresa e instituição?

---

## 2. O sistema é um verificador ou uma plataforma?

### Caminho 1 — Sistema verificador

- Receber dados  
- Validar  
- Gerar relatório  

### Caminho 2 — Plataforma completa

- Cadastro de estágio  
- Upload de contrato  
- Análise  
- Acompanhamento  
- Comunicação  
- Histórico  


### Definição sugerida

> O sistema será uma plataforma de apoio à gestão e verificação de estágios, com foco em conformidade legal, educacional e institucional.

---

## 3. Entradas, processamento e saídas

### Entradas
- Dados do aluno  
- Dados da empresa  
- Dados do estágio  
- Contrato  
- Plano de atividades  
- Regras institucionais  

### Processamento
- Leitura dos dados  
- Validação  
- Comparação com regras  
- Classificação  

### Saídas
- Relatório de conformidade  
- Pendências  
- Irregularidades  
- Decisão institucional  
- Notificações  

---

## 4. Estrutura em blocos

### 4.1 Entrada e cadastro
- Quem cadastra o estágio?  
- O aluno cadastra sozinho?  
- A empresa participa?  
- A instituição só revisa?  

---

### 4.2 Documentação
- Apenas PDF ou também DOCX?  
- O contrato será apenas anexado ou interpretado?  
- O plano de atividades será obrigatório?  

---

### 4.3 Motor de validação
- Quais regras são fixas?  
- Quais são configuráveis?  
- Valida apenas presença ou também coerência?  

---

### 4.4 Relatório e decisão
- O sistema só retorna status?  
- Explica os erros?  
- Sugere correções?  
- Quem aprova ou reprova?  

---

### 4.5 Comunicação
- Haverá notificações?  
- Existirá histórico de correções?  
- A empresa poderá reenviar documentos?  

---

## 5. Perguntas fundamentais do sistema

### 5.1 Usuário e fluxo
- Quem inicia o processo?  
- O aluno pode cadastrar sozinho?  
- A empresa precisa validar?  
- A instituição participa em qual etapa?  

---

### 5.2 Estágio
- É obrigatório ou não?  
- O aluno está matriculado?  
- Existe vínculo com o curso?  
- Há supervisor e professor orientador?  
- Existe plano de atividades?  
- Qual a carga horária?  
- Qual a duração?  

---

### 5.3 Empresa
- Existe convênio com a instituição?  
- Há responsável direto pelo estagiário?  
- Bolsa, transporte e seguro estão definidos?  

---

### 5.4 Instituição
- Usará apenas regras da lei ou regras próprias?  
- Aprovação será manual ou automática?  
- Regras mudam por curso?  

---

### 5.5 Contrato
- Será preenchido no sistema ou apenas anexado?  
- Haverá validação de campos antes do envio?  
- Haverá versionamento?  

---

## 6. Perguntas que o sistema precisa responder

O sistema deve responder:

- O estágio está conforme a Lei do Estágio?  
- O estágio atende aos critérios institucionais?  
- Existem pendências?  
- Existem irregularidades?  
- O estágio pode ser aprovado?  
- O que precisa ser corrigido?  
- Quem deve corrigir?  

---

## 7. Níveis de validação

### 7.1 Validação documental
- Contrato anexado  
- Plano de atividades  
- Supervisor informado  

---

### 7.2 Validação legal
- Carga horária  
- Bolsa  
- Transporte  
- Seguro  
- Duração  

---

### 7.3 Validação institucional
- Convênio  
- Professor orientador  
- Compatibilidade com o curso  
- Regras internas  

---

## Conclusão

O sistema deve funcionar como um **pipeline de verificação**, garantindo:

- Conformidade legal  
- Conformidade educacional  
- Organização do processo  
- Apoio à decisão institucional  

Esse modelo permite a construção de um sistema escalável e adaptável a diferentes instituições.