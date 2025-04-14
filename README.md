# Pythonic, 100% Open Source, Modern Data Stack, 2025

![Map Description](doc/map.png)

---

A forma como as empresas se relacionam com seus **dados** está mudando rapidamente e a
revolução dos **big data** evoluiu desde então, e já não é mais suficiente armazenar
seus enormes conjuntos de **dados** em um **data lake** para análise em **lote**.

**Velocidade** e **interconectividade** surgiram como os próximos grandes requisitos
competitivos de negócio, transformando novamente a forma como as empresas **criam**,
**armazenam**, **acessam** e **compartilham** seus dados importantes.

**Dados** são o sangue vital de um negócio. Mas muitas das formas como as empresas
**criam**, **compartilham** e **usam dados** são desorganizadas e desconectadas.

Este projeto tem o objetivo de fornecer uma estrutura abrangente para construir e
compartilhar **dados** por toda a organização, para que possamos fazer coisas úteis e
valiosas: melhor atendimento aos clientes, relatórios sem erros, **insights acionáveis**
e a viabilização de processos verdadeiramente **orientados por dados**, com foco em uma
_Modern Data Stack_, enfatizando boas práticas para arquiteturas modernas de dados —
como **Data Lakes**, **ELT**, **Data Warehouses**, **Data Mesh**, **Observabilidade**

---

# Conceitos de camadas de MDS

---

### **Camada 1 — Infraestrutura e Processamento (Próximo ao hardware)**

- **Cloud Platform (ex: AWS, GCP, Azure)**
- **Armazenamento bruto** (ex: Amazon S3, Google Cloud Storage, Data Lake)
- **Engine de computação** (ex: Spark, Dask, Snowflake engine, BigQuery engine)

---

### **Camada 2 — Ingestão de Dados**

- **ETL/ELT Tools** (ex: Fivetran, Airbyte, Meltano)
- Captura de dados de fontes (APIs, bancos relacionais, SaaS)

---

### **Camada 3 — Armazenamento e Modelagem**

- **Data Warehouse / Data Lakehouse** (ex: Snowflake, BigQuery, Redshift, Databricks)
- Armazenamento estruturado e modelagem de dados (ex: modelo estrela, Data Vault)

---

### **Camada 4 — Transformação e Orquestração**

- **Transformações SQL declarativas** (ex: dbt)
- **Orquestração de pipelines** (ex: Airflow, Prefect, Dagster)
- Controle de dependências e agendamento

---

### **Camada 5 — Ativação e Consumo**

- **Business Intelligence / Visualização** (ex: Looker, Tableau, Metabase, Power BI)
- **Reverse ETL / Operational Analytics** (ex: Census, Hightouch)
- **Data Apps / APIs** (ex: Streamlit, Retool, FastAPI)
- Aqui entra o **"browser" na sua analogia** – é onde o usuário final interage com os
  dados.

---

### **Camada 6 — Observabilidade, Segurança e Governança**

- **Monitoramento de dados e pipelines** (ex: Monte Carlo, Datafold, OpenLineage)
- **Catálogos e Linhagem de dados** (ex: Amundsen, DataHub, Atlan)
- **Governança, RBAC, mascaramento de dados** (ex: Immuta, Okera)

---

## No-code/Low-code:

O valor agregado está na camada de transformação e orquestração, onde o código
customizado pode definir as regras de negócios, garantir a qualidade dos dados e
automatizar processos complexos.

A automação e o surgimento de soluções no-code ou low-code podem reduzir a necessidade
de codificação em algumas áreas, especialmente na ingestão e visualização dos dados. A
codificação na camada de transformação e na criação de APIs e aplicativos customizados
continuará sendo um diferencial competitivo e uma fonte de inovação.

A maior parte do código customizado tende a ser produzido na camada de transformação e
orquestração, por ser nesta camada que se estabelecem as regras de negócio, a governança
dos dados e a escalabilidade dos pipelines. Há pontos estratégicos em outras camadas –
especialmente na ativação e consumo – onde o desenvolvimento também é crucial para criar
experiências diferenciadas e integrar os dados diretamente aos processos da empresa.

## Data Mesh

**Data Mesh** é uma forma de organizar a arquitetura de dados baseada em **domínios**.
Em vez de centralizar todos os dados em um **data lake** ou **data warehouse** gerido
por uma equipe única, o **Data Mesh** distribui a responsabilidade para os **times que
mais entendem os dados**: os times de produto ou áreas de negócio.

### Princípios do **Data Mesh**

1. **Domínio orientado à propriedade dos dados**  
   Cada time de domínio (ex: Vendas, Logística, Financeiro) é **responsável** por seus
   próprios dados como se fossem **produtos**.

2. **Dados como produto**  
   Os dados não são apenas subprodutos operacionais; eles devem ser tratados com a mesma
   seriedade de um produto de software — com qualidade, documentação e confiabilidade.

3. **Infraestrutura de dados como plataforma**  
   A organização fornece uma **plataforma de autoatendimento** que permite aos domínios
   publicarem, descobrirem e consumirem dados de forma **autônoma**, sem depender de
   times centrais.

4. **Governança federada**  
   A governança de dados é coordenada por princípios e padrões compartilhados, mas
   **executada de forma descentralizada**, garantindo **segurança, conformidade e
   interoperabilidade**.

---

## Processamento Analítico Online (OLAP)

Um sistema OLAP é uma tecnologia usada para análise rápida de grandes volumes de dados
multidimensionais. Ele permite que usuários explorem os dados de diferentes perspectivas
e níveis de detalhe, de forma interativa.

Os requisitos competitivos modernos dos **big data em movimento**, combinados com a
**computação em nuvem moderna**, exigem uma reavaliação de como as empresas **criam**,
**armazenam**, **movimentam** e **utilizam dados**. A base dessa nova **arquitetura de
dados** é o **evento**, o **quantum de dado** que representa atividades reais de
negócio, disponibilizado por meio de uma multiplicidade de **fluxos de eventos** criados
com finalidades específicas.

Os **fluxos de eventos** fornecem os meios para um verdadeiro **sistema nervoso
central**, permitindo que as unidades de negócio acessem e utilizem **blocos
fundamentais de dados autônomos e autoatualizáveis**.

Esses **blocos de dados** juntam-se aos pilares da modernidade tecnológica, como:

- **Containerização**
- **Infraestrutura como serviço (IaaS)**
- **Integração contínua (CI)** e **entrega contínua (CD)**
- Soluções de **monitoramento**

---

## Princípios para uma Modern Data Stack Sustentável

---

**1. Separação de responsabilidades**  
Divida pipelines e camadas de dados por função: **ingestão**, **transformação**,
**modelagem**, **consumo**. Isso facilita testes, reuso e evolução com menos atrito.

---

**2. Modularidade**  
Tenha componentes bem definidos: **ELT como serviço**, **catálogos de dados
desacoplados**, **módulos reutilizáveis de transformação** (ex: dbt models). Isso reduz
a **complexidade acidental** e melhora a escalabilidade.

---

**3. Ciclos de feedback rápidos**  
Automatize **testes de dados**, **validações de schema**, e **alertas proativos** com
ferramentas como **Great Expectations**, **Monte Carlo**, **OpenTelemetry** e **logs
estruturados**. Aprenda e ajuste antes que os usuários sintam o problema.

---

**4. Testes orientados ao uso**  
Teste os **dados que importam**: regras de negócios, KPIs críticos e integridade em
joins. Cobertura total é menos importante que testes **relevantes e eficazes**.

---

**5. Simplicidade com intenção**  
Evite soluções genéricas demais. Um **modelo simples e claro** que atende ao caso de uso
real é melhor do que um pipeline genérico, difícil de manter. **Exploração guiada por
necessidade** é chave em domínios de dados complexos.

---

**6. Overengineering é dívida técnica disfarçada**  
Adicionar múltiplas ferramentas, camadas ou abstrações sem uma razão clara **gera
acúmulo de dívida técnica**.  
**Dívida técnica**, no contexto de dados, é qualquer **comprometimento com soluções
frágeis, mal documentadas ou difíceis de evoluir** que **aumentam o custo** de
manutenção, aprendizado de novos membros, adaptação a novas demandas e auditorias de
dados.

---

**7. Boas abstrações reduzem ruído, não clareza**  
Crie **camadas de visualização e acesso aos dados** que ajudem os usuários a tomar
decisões — sem esconder a lógica ou complexidade que importa. Más abstrações causam
**falsas interpretações** e **confiança indevida nos dados**.

---

**8. Comunicação clara é infraestrutural**  
**Data contracts**, **nomenclatura padrão**, **documentação acessível**, **commits
explicativos** e **linha do tempo de transformações** são tão importantes quanto código
ou queries. Promovem **confiança e colaboração entre times**.

---

**9. Pensamento em trade-offs é essencial**  
Armazenar tudo em tempo real? Pode ser caro e desnecessário. Pré-agregar tudo? Pode
perder flexibilidade.  
**Engenheiros e arquitetos de dados maduros entendem o custo-benefício de cada decisão**
e não buscam uma “solução única ideal”.

---

**10. Aprendizado contínuo como rotina**  
O ecossistema de dados muda rápido. Times que **experimentam**, **testam novas
ferramentas com critérios claros**, e se mantêm **curiosos**, criam soluções mais
resilientes e adaptáveis. Não se trata de saber tudo, mas de saber **o que testar e o
que priorizar**.

---

### Migrations

`./packages/warehouse_migrations` usa [Alembic](https://alembic.sqlalchemy.org/) para
gerenciar migrations do modelo definido em `./packages/warehouse_objects`

INFO: Doc de uso no README do componente.

## Packages

#### Python Libs

Cada Lib e um `uv workspace`

- warehouse_objects: ORM da plataforma

> [!IMPORTANT] Requer o uso de [uv](https://docs.astral.sh/uv/) para Python environment.

## Cluster config (Docker Compose)

- PostgreSQL: postgresql://postgres:postgres@localhost:5432/appdb
- Valley: redis://localhost:6379
- Supabase: http://localhost:3000
- Superset: http://localhost:8088

## Install

TODO: escrever o roteiro de novas instalacoes

    git clone ...

    cd ...

    git submodule update --init --recursive

Copy the fake env vars

    cp .env.example .env

Pull the latest images

    docker compose pull

Start the services (in detached mode)

    docker compose up -d
