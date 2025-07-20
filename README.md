# POC: Comparação entre Go com Apache Beam e Python com Apache Spark para Pipelines de Dados

## 1. Objetivo

Esta Prova de Conceito (POC) tem como objetivo avaliar e comparar duas abordagens modernas para a construção de pipelines de dados: **Go com Apache Beam** e **Python com Apache Spark**. A análise considera aspectos cruciais como:

* Velocidade de ingestão de dados
* Capacidade de lidar com operações de processamento complexas
* Facilidade de implementação e manutenção
* Suporte a múltiplos formatos de arquivos
* Adequação ao mercado profissional

Ao final, a POC buscará identificar qual abordagem oferece o melhor equilíbrio entre performance, escalabilidade e produtividade para apoiar decisões técnicas mais assertivas no projeto.

---

## 2. Motivação

A crescente demanda por soluções escaláveis, performáticas e flexíveis no processamento de dados impõe desafios importantes para times de engenharia. Diante disso, torna-se essencial escolher tecnologias que não apenas atendam aos requisitos técnicos, mas que também sejam sustentáveis no longo prazo.

Esta POC surge da necessidade de testar, na prática, alternativas modernas ao modelo tradicional de pipelines, considerando linguagens emergentes como Go, aliadas a frameworks robustos como Apache Beam. Ao mesmo tempo, exploramos a maturidade e o ecossistema consolidado do Apache Spark com Python, amplamente adotado na indústria.

A iniciativa visa embasar a escolha tecnológica com evidências concretas, permitindo decisões mais fundamentadas e alinhadas com os objetivos do projeto, promovendo inovação com responsabilidade técnica.

---

## 3. Escopo da POC

* **Formatos de entrada:** CSV, JSON, Parquet, Avro, XML, ORC e Delta
* **Operações a serem avaliadas:** agregações, joins, filtros complexos
* **Volumes de teste:** 1 GB e 10 GB
* **Fora do escopo:** integrações externas, segurança e orquestração

---

## 4. Critérios de Avaliação e Métricas

### 4.1 Velocidade de Ingestão

* **Métrica:** Tempo total de ingestão (em segundos)
* **Como medir:** Cronometrar o tempo de execução dos pipelines
* **Ferramentas:** Logs, profiler, ferramentas de monitoramento de sistema

### 4.2 Capacidade de Processamento Complexo

* **Métrica:** Tempo de execução de operações complexas
* **Como medir:** Implementar e medir o tempo de execuções específicas
* **Avaliação qualitativa:** Facilidade de implementação e legibilidade do código

### 4.3 Facilidade de Implementação Multiformato

* **Métrica:** Tempo de desenvolvimento (horas/dias)
* **Avaliação qualitativa:** Qualidade da documentação, suporte da comunidade e bibliotecas disponíveis

### 4.4 Viabilidade de Mercado

* **Métrica qualitativa:**

  * Volume de vagas no mercado relacionadas a Go/Beam e Spark
  * Tamanho da comunidade, treinamentos, eventos e materiais disponíveis

---

## Setup e Execução do Ambiente

Todos os scripts e instruções para preparar o ambiente, instalar dependências e baixar o dataset de teste estão localizados na pasta `prep_ambiente`.

**➡️ Acesse o guia de preparação do ambiente local**

Como alternativa à configuração manual, você pode usar um ambiente Docker pré-configurado. As instruções estão na pasta `infra`. **➡️ Acesse o guia de preparação do ambiente Docker**

---

## 5. Plano de Execução

| Etapa                 | Descrição                                   | Responsável | Prazo |
| --------------------- | ------------------------------------------- | ----------- | ----- |
| Levantamento de dados | Obter datasets de referência                |             |       |
| Implementação Go      | Desenvolver o pipeline utilizando Go + Beam |             |       |
| Implementação Spark   | Desenvolver o pipeline com Python + Spark   |             |       |
| Testes de performance | Executar e coletar métricas                 |             |       |
| Análise de mercado    | Levantamento de dados e tendências          |             |       |
| Documentação final    | Consolidação dos resultados e conclusões    |             |       |

---

## 6. Ferramentas e Tecnologias

* **Go:** (versão), bibliotecas utilizadas (ex: `encoding/csv`, `parquet-go`)
* **Apache Spark:** (versão), linguagem (PySpark ou Scala)
* **Ambiente:** Descrição da infraestrutura de execução e testes

---

## 7. Riscos e Mitigações

| Risco                                                                    | Mitigação                                                        |
| ------------------------------------------------------------------------ | ---------------------------------------------------------------- |
| Diferenças de maturidade entre as bibliotecas podem afetar os resultados | Documentar as limitações e ajustar os testes conforme necessário |
| Curva de aprendizado do Spark pode aumentar o tempo de desenvolvimento   | Adotar exemplos práticos e documentação oficial como apoio       |
| Infraestrutura desigual pode enviesar os resultados                      | Garantir equivalência de recursos computacionais nos testes      |

---

## 8. Conceito dos Formatos de Arquivo

**1. CSV (Comma Separated Values)**

* Formato simples baseado em texto
* Ampla compatibilidade com sistemas
* Pouco eficiente para análises em larga escala

**2. JSON (JavaScript Object Notation)**

* Baseado em texto, legível por humanos
* Ideal para troca de dados entre sistemas heterogêneos
* Suportado amplamente em APIs e aplicações web

**3. Parquet (Formato colunar)**

* Otimizado para leitura de colunas específicas
* Alta taxa de compressão e eficiência para Big Data
* Preserva tipagem e é compatível com ecossistemas como Spark, Hive

**4. Avro (Formato binário)**

* Binário, compacto e com suporte a esquemas
* Alta compatibilidade com sistemas Hadoop
* Ideal para transporte e serialização de dados

**5. XML (Extensible Markup Language)**

* Estrutura hierárquica com tags personalizadas
* Suportado em diversas plataformas
* Mais verboso que JSON, porém mais flexível em estrutura

**6. ORC (Optimized Row Columnar)**

* Formato colunar otimizado para Hive/Spark
* Alta compressão e performance de leitura
* Suporte a estatísticas e tipos complexos

**7. Delta (Delta Lake)**

* Baseado em Parquet com suporte a transações ACID
* Ideal para cenários com atualização e versionamento de dados
* Usado em pipelines incrementais e processamento de dados em tempo real

---

## 9. Tabela Comparativa de Formatos

| Formato     | Características Principais          | Uso Típico                                       |
| ----------- | ----------------------------------- | ------------------------------------------------ |
| **CSV**     | Texto simples, baixa eficiência     | Pequenos conjuntos de dados, interoperabilidade  |
| **JSON**    | Texto estruturado, legível e leve   | Integração entre sistemas, APIs                  |
| **Parquet** | Colunar, eficiente e comprimido     | Big Data e consultas analíticas                  |
| **Avro**    | Binário, com esquema e compacto     | Serialização de dados em pipelines               |
| **XML**     | Estrutura hierárquica e flexível    | Intercâmbio de dados em sistemas legados         |
| **ORC**     | Colunar com compressão eficiente    | Hive e Spark para grandes volumes                |
| **Delta**   | Controle de versão, transações ACID | Data Lakes dinâmicos e pipelines com atualização |

---

## 10. Dataset Base

Será utilizado como base de testes o dataset público do Kaggle:
🔗 [State of Data - Brazil 2023](https://www.kaggle.com/datasets/datahackers/state-of-data-brazil-2023)

Este conjunto será processado pelo script `geraDados.py`, que gerará versões com tamanhos de **1 GB** e **10 GB** nos diferentes formatos listados acima.
