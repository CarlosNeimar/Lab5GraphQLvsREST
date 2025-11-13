# Análise comparativa da performance de web APIs GraphQL vs REST

## 1. Introdução

Neste trabalho, realizou-se um experimento controlado com o objetivo de comparar a performance de APIs web quando implementadas em GraphQL versus REST. A fim de nortear este estudo, foram estabelecidas as seguintes questões de pesquisa:

- **RQ 01**: Respostas às consultas GraphQL são mais rápidas que respostas às consultas REST?
- **RQ 02**: Respostas às consultas GraphQL tem tamanho menor que respostas às consultas REST?

## 2. Design do experimento

O experimento foi elaborado visando assegurar a validade dos resultados e responder às questões de pesquisa propostas. Para isso, foram definidos hipóteses, variáveis dependentes e independentes, além de tratamentos que representam as combinações de condições a serem comparadas.

#### 1. Hipóteses Nula e Alternativa

|                           | RQ 01                                               | RQ 02                                                   |
| ------------------------- | --------------------------------------------------- | ------------------------------------------------------- |
| Hipótese nula (H₀)        | Não há diferença significativa no tempo de resposta | Não há diferença significativa no tamanho das respostas |
| Hipótese alternativa (Hₐ) | GraphQL tem tempos de resposta menores              | GraphQL tem respostas menores                           |

#### 2. Variáveis Dependentes

- **RQ 01**: Tempo de resposta (em ms)
- **RQ 02**: Tamanho do `response body` (em número de caracteres)

#### 3. Variáveis Independentes

| Fator                        | Níveis               |
| ---------------------------- | -------------------- |
| Tipo de implementação de API | `GraphQL`, `REST`    |
| Linguagem                    | `JavaScript`, `Python` |

#### 4. Tratamentos

1. API implementada em GraphQL com JavaScript
2. API implementada em REST com JavaScript
3. API implementada em GraphQL com Python
4. API implementada em REST com Python
