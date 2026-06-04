---
id: documento_de_visao
title: Documento de Visão
---
## Introdução

O VerificaEstagio é um backend Django REST para cadastro e validação de contratos de estágio. Este documento descreve o problema, a proposta de solução, os objetivos do produto e os limites do sistema com base no que já foi implementado.

## Descrição do problema

A análise de contratos de estágio costuma ser manual, fragmentada entre aluno, empresa e instituição de ensino, e sujeita a erros de conformidade. Sem um fluxo automatizado, pendências essenciais podem passar despercebidas, atrasando a aprovação do estágio.

### Problema

Não existe um sistema centralizado que:
- registre estágio e contrato de forma integrada;
- valide regras obrigatórias de estágio (carga horária, seguro, supervisor, professor orientador e plano de atividades);
- gere pendências e relatórios de conformidade;
- permita emissão de parecer institucional sobre o contrato.

### Impactados

- Estudantes / usuários que precisam validar contratos de estágio;
- Empresas que oferecem vagas de estágio;
- Instituições de ensino responsáveis pela aprovação;
- Coordenadores e analistas de estágio.

### Consequência

- Contratos podem ser aceitos sem requisitos legais completos;
- pendências não são registradas nem monitoradas;
- aprovações ficam dispersas entre sistemas diferentes;
- falta transparência no status do processo.

### Solução

Criar o VerificaEstagio como uma API para:
- cadastrar usuários, empresas, instituições, estágios e contratos;
- permitir upload de contratos em PDF;
- aplicar regras de negócio definidas para análise de estágio;
- gerar análises, pendências e relatórios de conformidade;
- atualizar o status do contrato e registrar parecer institucional.

## Objetivos

- Disponibilizar um backend funcional para gestão de contratos de estágio;
- implementar validação automática de regras de estágio;
- produzir análises e relatórios de conformidade;
- suportar a emissão de parecer institucional;
- fornecer uma base sólida para frontends ou integrações futuras.

## Descrição do usuário

Os usuários esperados são:
- alunos/estagiários que submetem contratos;
- responsáveis de empresas que cadastram ou associam contratos;
- instituições de ensino que analisam e aprovam contratos;
- analistas que consultam pendências e relatórios.

## Recursos do produto

### Autenticação e cadastro

- Registro de usuário Django.
- Login e logout via sessão.
- CRUD de usuários, empresas e instituições.

### Gestão de estágio

- Cadastro de estágio vinculado a usuário, empresa e instituição.
- Regras de validação para carga horária, seguro, supervisor, orientador e plano de atividades.

### Gestão de contratos

- Cadastro de contrato e relacionamento com estágio.
- Upload de arquivo PDF validado.
- Análise automática de conformidade e atualização de status.

### Análise e relatórios

- Criação de análises com resultado aprovado, pendente ou reprovado.
- Geração de pendências detalhadas.
- Geração de relatório textual de conformidade.

### Parecer institucional

- Registro de parecer de instituição de ensino.
- Atualização do contrato para APROVADO_FINAL ou INVALIDO_PENDENTE.

## Restrições

- Projeto atual é apenas backend; não existe frontend completo no repositório.
- OCR de contrato está presente como stub e não realiza extração real de texto.
- Arquivos de contrato devem ser enviados em formato PDF.
- O banco de dados utilizado é SQLite por padrão.
- Não há envio automático de notificações ou e-mails no código atualmente.

## Status atual

- Implementado: cadastro de recursos, autenticação, upload de PDF, análise automática, geração de pendências, relatório de conformidade, parecer institucional.
- Em desenvolvimento ou não implementado: OCR real de documentos, notificações por e-mail, interface de usuário, confirmação de cadastro por e-mail, dashboard de acompanhamento.

## Versionamento
| Data | Versão | Descrição | Autor(es) |
| -- | -- | -- | -- |
| 04/06/2026 | 1.0 | Documento de visão alinhado ao backend atual | Pedro Santos, Gabriel Melo, Bernardo Brandao, Iago Viana, Gabriel Maccachero | 

