# Análise comparativa da performance entre APIs GraphQL vs REST

## 1. Introdução

A linguagem de consulta GraphQL, proposta pelo Facebook como metodologia de implementação de APIs Web, representa uma alternativa às populares APIs REST. Baseada em grafos, a linguagem permite que usuários consultem banco de dados na forma de schemas, de modo que se possa exportar a base e realizar consultas num formato definido pelo fornecedor da API. Por outro lado, APIs criados com base em abordagens REST baseiam-se em endpoints: operações pré-definidas que podem ser chamadas por clientes que desejam consultar, deletar, atualizar ou escrever um dado na base. Desde o seu surgimento, vários sistemas realizaram a migração entre ambas as soluções, mantendo soluções compatíveis REST, mas oferecendo os benefícios da nova linguagem de consulta proposta. Entretanto, não está claro quais os reais benefícios da adoção de uma API QraphQL em detrimento de uma API REST. Nesse contexto, o objetivo deste laboratório é realizar um experimento controlado para valiar quantitativamente os benefícios da adoção de uma API GraphQL. Especificamente, as seguintes perguntas devem ser respondidas: 

- **RQ 01**: Respostas às consultas GraphQL são mais rápidas que respostas às consultas REST?
- **RQ 02**: Respostas às consultas GraphQL tem tamanho menor que respostas às consultas REST?

## 2. Design do experimento

#### 1. Hipóteses Nula e Alternativa

|                           | RQ 01                                               | RQ 02                                                   |
| ------------------------- | --------------------------------------------------- | ------------------------------------------------------- |
| Hipótese nula (H₀)        | Não há diferença significativa no tempo de resposta | Não há diferença significativa no tamanho das respostas |
| Hipótese alternativa (Hₐ) | GraphQL tem tempos de resposta menores              | GraphQL tem respostas menores                           |

#### 2. Variáveis Dependentes

- **RQ 01**: Tempo de resposta (em ms) medido do lado do cliente
- **RQ 02**: Tamanho do `response body` (em número de caracteres)

#### 3. Variáveis Independentes

| Fator                        | Níveis               |
| ---------------------------- | -------------------- |
| Tipo de implementação de API | `GraphQL`, `REST`    |
| Linguagem                    | `JavaScript`, `Python` |

#### 4. Tratamentos

1. API implementada em GraphQL com JavaScript (Node.js)
2. API implementada em REST com JavaScript (Node.js)
3. API implementada em GraphQL com Python (Flask)
4. API implementada em REST com Python (Flask)

#### 5. Objetos Experimentais

Os objetos experimentais consistem em duas pequenas aplicações de back-end (uma em Flask e uma em Node.js). Ambas as aplicações implementarão as duas arquiteturas (REST e GraphQL) e acessarão uma base de dados local comum.

Serão testados cenários de leitura e também de escrita inclusão, alteração e deleção, permitindo comparar Query (GraphQL) vs GET (REST) e Mutation (GraphQL) vs POST/PUT/DELETE (REST).

#### 6. Tipo de Projeto Experimental

Analisar o efeito principal de cada variável independente (Tipo de API, Linguagem) e também o efeito de interação entre elas, por exemplo se a diferença de performance entre REST e GraphQL depende da linguagem utilizada.

#### 7. Quantidade de Medições

Para cada um dos 4 tratamentos, será executada uma bateria de 100 requisições automatizadas para cada cenário de teste. O experimento será repetido 10 vezes para garantir a estabilidade dos dados, minimizando vieses de caching ou flutuações momentâneas do sistema. A análise estatística será feita sobre a média e mediana das medições.

#### 8. Ameaça a validade

- Ameaça: Execução de outros processos na máquina local pode interferir no tempo de resposta.

- Mitigação: O experimento será executado em ambiente controlado, com o mínimo de processos concorrentes. A base de dados será redefinida para o mesmo estado inicial antes de cada rodada de testes.

- Ameaça: A implementação de uma API (ex: REST) pode ser mais otimizada que a outra (ex: GraphQL) de forma não intencional.

- Mitigação: As consultas ao banco de dados e a lógica de negócio serão o mais similares possível em ambas as implementações.

- Ameaça: Os resultados podem não ser generalizáveis para aplicações em larga escala, com redes complexas ou com lógicas de negócio muito diferentes.

- Mitigação: Esta é uma limitação conhecida. O foco do estudo é a performance técnica da arquitetura em um cenário padronizado e local.

## 3. Preparação do Experimento

Configuração de ambiente necessária para a execução dos testes e coleta de dados.

#### Desenvolvimento das APIs:

- Criação da aplicação back-end em Python (Flask) utilizando Flask-RESTful e Graphene ou para GraphQL.

- Criação da aplicação back-end em JavaScript (Node.js) utilizando Express (para REST) e Apollo Server GraphQL.

- Garantir que ambas as aplicações se conectem à mesma base de dados.

#### Configuração da Base de Dados:

- Base de dados MySQL local

- Definição de um schema unificado.

- Carga de dados de mock utilizada no Laboratório 4 e disciplina TI6.

#### Desenvolvimento de Scripts de Teste:

- Criação de scripts para automatizar a execução de requisições dos 4 mecanismos.

- Realizar consultas de leitura.

- Realizar consultas de escrita.

- Capturar as métricas (tempo de resposta e tamanho do body) para cada requisição.

#### Coleta de Dados:

- Os resultados das medições serão persistidos de forma estruturada em um arquivo CSV