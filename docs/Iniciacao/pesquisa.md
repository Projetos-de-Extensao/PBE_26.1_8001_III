---
id: pesquisa
title: Pesquisa
---

# Pesquisa

# Guia de Estágios

## 1. Objetivo do Estágio
O estágio é visto como uma porta de entrada para o mercado, focado no desenvolvimento de habilidades práticas e como um complemento essencial da formação acadêmica.

## 2. Tipos de Estágio
* **Estágio obrigatório:** Faz parte da grade curricular e é requisito indispensável para a graduação.
* **Estágio não obrigatório:** Atividade opcional, realizada como complemento à formação.

## 3. Documentação Necessária
Para a formalização do estágio, são exigidos:
1.  **Termo de Compromisso de Estágio (TCE)**
2.  **Convênio** entre a empresa e a instituição de ensino
3.  **Plano de atividades** detalhado

## 4. Plano de Atividades
O estágio deve possuir objetivos claros de aprendizado. Todas as atividades devem ser previamente definidas para garantir o foco educativo.

## 5. Acompanhamento
É obrigatório o acompanhamento sistemático tanto pela **instituição** quanto pela **empresa**, incluindo a realização de avaliações periódicas de desempenho.

## 6. Responsabilidades
| Ator | Responsabilidade |
| :--- | :--- |
| **Instituição** | Valida a documentação e acompanha o progresso acadêmico. |
| **Empresa** | Oferece o ambiente de aprendizado e supervisiona as tarefas. |
| **Aluno** | Cumpre as atividades acordadas e segue o plano de estágio. |

## 7. Compatibilidade com o Curso
As atividades práticas desenvolvidas no ambiente de trabalho devem estar estritamente relacionadas à área de formação do aluno.

## 8. Validação do Estágio
A instituição de ensino possui a prerrogativa de **aprovar**, **reprovar** ou **exigir ajustes** no estágio, baseando-se nos critérios acadêmicos.

## 9. Comparação com a Lei do Estágio
* **Lei do Estágio:** Foca primordialmente nos direitos trabalhistas, limites de carga horária e formalização contratual.
* **Ibmec:** Foca na qualidade do aprendizado, desenvolvimento de competências e validação do conteúdo acadêmico.

!!! tip "10. Insights para Sistemas"
    Para o desenvolvimento de plataformas de gestão, os seguintes pontos são essenciais:
    * Mecanismos de **validação do plano de atividades**.
    * Verificação automática de **compatibilidade com o curso**.
    * Fluxos de **integração institucional** (assinaturas digitais e workflows de aprovação).

# Diretrizes de Validação de Estágio - Ibmec

As diretrizes gerais para a validação de estágio no Ibmec seguem a Lei do Estágio (Lei nº 11.788/2008) para garantir que a experiência no mercado de trabalho contribua para a sua formação acadêmica.

## Principais Diretrizes e Requisitos

* **Vínculo com o Curso:** As atividades desenvolvidas no estágio precisam estar alinhadas com a sua formação acadêmica e ser compatíveis com o projeto pedagógico do seu curso.
* **Termo de Compromisso:** A formalização é essencial. É obrigatório ter o Termo de Compromisso de Estágio (TCE) assinado pela empresa contratante, por você (aluno) e pelo Ibmec.
* **Período Autorizado:** O estágio costuma ser autorizado a partir do 4º período, mas isso pode variar de acordo com o seu curso específico.
* **Documentação Obrigatória:** Para que a validação aconteça, você precisará entregar a Avaliação de Desempenho do estagiário e o Relatório Final de Estágio.
* **Comprovação de Vínculo:** Em alguns casos, pode ser solicitada a cópia do registro na carteira de trabalho ou o contrato social.

## Validação como Atividades Complementares

As horas que você cumpre no estágio podem ser aproveitadas e contabilizadas como Atividades Acadêmicas Complementares (AAC). Para isso, é necessário fazer a comprovação diretamente com a coordenação do seu curso.

## Passo a Passo do Procedimento

1. **Formalização:** Assine o TCE *antes* de começar a trabalhar.
2. **Acompanhamento:** Você terá o acompanhamento técnico de um supervisor na empresa e, se necessário, de um professor orientador do Ibmec.
3. **Avaliação:** O seu supervisor na empresa precisará preencher um relatório de atividades e uma ficha de avaliação.
4. **Aprovação Final:** A coordenação do curso irá avaliar toda a documentação e o relatório para dar o parecer final da validação.

# Sistema de Verificação

## 1. Objetivo do Sistema

Desenvolver um sistema web em Python com Django para analisar contratos de estágio, validar conformidade com a Lei do Estágio e diretrizes educacionais, e gerar relatórios automáticos.

## 2. Perfis de Usuário

- Aluno
- Empresa
- Instituição
- Administrador

## 3. Fluxo Principal do Sistema

1. Login do usuário
2. Cadastro do estágio
3. Upload do contrato
4. Leitura dos dados
5. Validação automática
6. Geração de relatório
7. Análise institucional
8. Aprovação, reprovação ou pendência

## 4. Estrutura de Módulos

- Autenticação
- Cadastro institucional
- Cadastro de estágio
- Upload de contrato
- Extração de dados
- Motor de validação
- Relatórios
- Aprovação institucional

## 5. Modelagem do Banco de Dados

Entidades principais:

- Usuário
- Curso
- Empresa
- Estágio
- Contrato
- Regra
- Validação
- Pendência

## 6. Regras de Validação

- Carga horária máxima de 6h/dia e 30h/semana
- Estágio não obrigatório exige bolsa e transporte
- Seguro obrigatório
- Supervisor e professor orientador obrigatórios
- Plano de atividades necessário
- Duração máxima de 2 anos

## 7. Lógica do Sistema

O sistema analisa os dados cadastrados e compara com regras, retornando um dos seguintes status:

- aprovado
- pendente
- irregular

## 8. Estrutura Técnica (Django)

Apps sugeridos:

- `accounts`
- `core`
- `internships`
- `validation`
- `reports`

## 9. Exemplo de Lógica em Python

A função `validar_estagio()` compara os dados do estágio e retorna um status baseado em erros e pendências.

```python
def validar_estagio(estagio):
    erros = []
    pendencias = []

    if estagio.carga_horaria_dia > 6:
        erros.append("Carga horária diária acima do permitido.")

    if estagio.carga_horaria_semana > 30:
        erros.append("Carga horária semanal acima do permitido.")

    if estagio.tipo_estagio == "nao_obrigatorio":
        if not estagio.bolsa:
            erros.append("Estágio não obrigatório sem bolsa.")
        if not estagio.auxilio_transporte:
            erros.append("Estágio não obrigatório sem auxílio-transporte.")

    if not estagio.seguro:
        erros.append("Seguro obrigatório não informado.")

    if not estagio.supervisor:
        pendencias.append("Supervisor não informado.")

    if not estagio.professor_orientador:
        pendencias.append("Professor orientador não informado.")

    if not estagio.plano_atividades:
        pendencias.append("Plano de atividades não anexado.")

    if erros:
        status = "irregular"
    elif pendencias:
        status = "pendente"
    else:
        status = "aprovado"

    return {
        "status": status,
        "erros": erros,
        "pendencias": pendencias,
    }