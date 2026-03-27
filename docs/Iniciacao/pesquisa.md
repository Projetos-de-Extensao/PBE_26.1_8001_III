---
id: pesquisa
title: Pesquisa
---

# Pesquisa

## 2. Diretrizes do MEC (LDB e CNE)

O estágio é definido como parte integrante do processo educacional, devendo obrigatoriamente estar vinculado ao currículo do curso.

### Base Legal
!!! info "Fundamentação Jurídica"
    * **LDB:** Lei de Diretrizes e Bases da Educação Nacional (Lei nº 9.394/96).
    * **DCNs:** Diretrizes Curriculares Nacionais.

### Papel da Instituição de Ensino
A instituição tem o dever de garantir o caráter pedagógico do estágio através de:
* [x] **Acompanhamento e validação** contínua.
* [x] **Designação de professor orientador** específico.
* [x] **Avaliação de relatórios periódicos** entregues pelo aluno.

### Supervisão Obrigatória
O estágio só é válido se houver dupla supervisão:
1.  **Professor Orientador:** Representando a faculdade.
2.  **Supervisor:** Profissional da empresa com formação na área.

### Tipos de Estágio e Compatibilidade
* **Obrigatório:** Previsto no currículo e necessário para diplomação.
* **Não obrigatório:** Atividade complementar para ganho de experiência.
* **Alinhamento:** As atividades **devem** estar estritamente alinhadas com a área de formação.

!!! failure "Validação Acadêmica"
    A instituição possui autonomia para **invalidar** o estágio caso identifique que não há valor pedagógico real nas atividades executadas.

---

## 3. Principais Nuances e Brechas

É fundamental monitorar pontos que podem descaracterizar o estágio legalmente:

* **Desvio de Função:** Quando o estagiário executa atividades operacionais de um funcionário CLT, perdendo o foco no aprendizado.
* **Falta de Supervisão Real:** Estagiários que trabalham isolados, sem orientação de um profissional qualificado.
* **Atividades Incompatíveis:** Tarefas que não possuem relação direta com a grade curricular do curso.

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