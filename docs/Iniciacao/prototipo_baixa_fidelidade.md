---
id: prototipobaixa
title: Protótipo Baixa Fidelidade
---
## Introdução

<p align = "justify">
A construção do protótipo de alta fidelidade auxilia a equipe de desenvolvimento a encontrar um nível de detalhes abrangentes, extrair funcionalidades, testar usabilidade, e também fornece uma base para o gerenciamento do projeto pois com o protótipo é possível realizar estimativas de quanto tempo será necessário desempenhar em cada funcionalidade.
</p>

## Metodologia

<p align = "justify">
Iniciamos o projeto através dos levantamentos iniciais da equipe, após discussões a ferramenta Figma foi selecionada para produzir o protótipo de alta fidelidade com auxílio do Material Design Color Tool.
</p>

## Protótipo de baixa fidelidade

### Versão 1.0

### Tela Login

```plantuml
@startsalt
{+
  <b>Plataforma de Gestao de Estagios - Ibmec
  ==
  Login 
  | "matricula@alunos.ibmec.edu.br"
  Senha 
  | "*******"
  [ Entrar ]
  --
  [x] Lembrar-me
  [Esqueci minha senha]
}
@endsalt
```

### Dashboard do Aluno

```plantuml
@startsalt
{+
  <b>Bem-vindo, Aluno! | [ Sair ]
  ==
  Meus Estagios:
  {#
    Empresa | Status | Acao
    Tech Solutions | [Irregular] | [ Ver Detalhes ]
    Inovacao S.A.  | [Aprovado]  | [ Ver Detalhes ]
  }
  --
  [ + Novo Cadastro de Estagio ]
}
@endsalt
```

### Tela de Cadastro de Dados do Estágio

```plantuml
@startsalt
{+
  <b>Encerramento de Estagio - Envio de Documentos
  ==
  Aluno:*******
  Empresa: Tech Solutions
  --
  <b>1. Relatorio Final de Estagio:
  [ Escolher arquivo ] 
  | "Relatorio_Final_aluno.pdf"
  --
  <b>2. Avaliacao de Desempenho (Preenchida pelo Supervisor):
  [ Escolher arquivo ] 
  | "Avaliacao_TechSolutions_Assinada.pdf"
  --
  <b>3. Comprovante de Rescisao / Fim de Contrato (Opcional):
  [ Escolher arquivo ] 
  | "Nenhum arquivo selecionado"
  --
  [ Cancelar ] 
  [ Enviar para Analise da Coordenacao ]
}
@endsalt
```

### Tela de Envio de Documentos (Upload)

```plantuml
@startsalt
{+
  <b>Envio de Documentos
  ==
  Termo de Compromisso (TCE):
  [ Escolher arquivo ] 
  | "TCE_aluno_Assinado.pdf"
  --
  Plano de Atividades:
  [ Escolher arquivo ] 
  | "Nenhum arquivo selecionado"
  --
  [ Cancelar ] 
  | [ Enviar para Validacao ]
}
@endsalt
```

### Visão da Instituição (Painel da Coordenação)

```plantuml
@startsalt
{+
  <b>Painel de Aprovacao Institucional
  ==
  Filtro de Status: Pendentes
  {#
    Aluno | Curso | Status Motor | Acao
    Gabriel Melo | Eng. Software | [Pendente] | [ Analisar ]
    Joao Silva   | Direito       | [Irregular] | [ Analisar ]
  }
}
@endsalt
```

### Relatório de Validação (Resultado do Motor)

```plantuml
@startsalt
{+
  <b>Relatorio de Validacao Automatica
  ==
  Aluno: ************
  Empresa: Tech Solutions
  --
  <b>Status Final: [ IRREGULAR ]
  --
  Erros Encontrados:
  * Carga horaria semanal acima do permitido.
  * Estagio nao obrigatorio sem bolsa.
  Pendencias:
  * Plano de atividades nao anexado.
  --
  Decisao Institucional:
  () Aprovar  () Reprovar  (X) Solicitar Correcao
  --
  [ Notificar Aluno ] | [ Voltar ao Painel ]
}
@endsalt
```

## Conclusão

<p align = "justify">
A partir da elaboração do protótipo foi possível ter uma noção inicial da interface do usuário, definindo fluxo, paleta de cores, botões, app bars e diversas outras funcionalidades
</p>

## Referências

> Ferramenta PlantUML. Disponível em (https://plantuml.com/salt)

## Autor(es)

| Data | Versão | Descrição | Autor(es) |
| -- | -- | -- | -- |
| 16/04/2026 | 1.0 | Criação do documento | Gabriel Melo,Bernardo Brandão,Iago Viana,Pedro Dos Santos e Gabriel m| 
