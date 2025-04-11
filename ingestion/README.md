## Linhagem de dados

(ou _data lineage_) é o rastreamento completo do ciclo de vida dos dados: desde a sua
origem, passando por todas as transformações, movimentações e usos, até o destino final.

Ela responde perguntas como:

- De onde vieram esses dados?
- Que processos os transformaram?
- Quais sistemas os consumiram?
- O que mudou ao longo do tempo?

A linhagem é essencial para garantir **transparência**, **confiabilidade**,
**auditoria**, **governança de dados** e facilitar a **resolução de erros** e **impact
analysis** (ex.: “se eu alterar esse campo, o que será afetado?”).

Ferramentas automatam esse rastreamento, mantendo um histórico detalhado de como os
dados fluem nos pipelines.

## Marquez

[Marquez](https://github.com/MarquezProject/marquez/) permite consultas altamente
flexíveis de _data lineage_ (linhagem de dados) em todos os conjuntos de dados,
associando com eficiência e confiabilidade as dependências entre jobs e os dados que
produzem e consomem.

**Por que gerenciar e utilizar metadados?**  
Gerenciar metadados é essencial para rastrear, descobrir e entender como os dados fluem
e se transformam ao longo do tempo.

**Design**  
Marquez é modular, escalável, extensível e agnóstico à plataforma. Seus componentes
incluem:

- **Repositório de Metadados**: Armazena dados sobre jobs, datasets e histórico de
  execuções.
- **API de Metadados**: Interface RESTful para registrar e consultar metadados.
- **UI de Metadados**: Interface para descoberta de datasets e visualização de
  dependências.

Marquez adota a especificação **OpenLineage**, com suporte a Java, Python e diversas
integrações.

**Modelo de Dados**  
O modelo é baseado em imutabilidade e registros temporais.

- **Job**: Tem dono, nome, versão e define datasets de entrada/saída.
- **Versão de Job**: Imutável, ligada ao código fonte e associada a datasets.
- **Dataset**: Tem dono, nome, schema, versão e pertence a uma fonte de dados.
- **Versão de Dataset**: Imutável e com ID único para preservar seu estado ao longo do
  tempo.
