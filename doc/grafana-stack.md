# Grafana Stack no Contexto de uma Arquitetura Modern Data Stack (MDS)

A Grafana Stack se posiciona na camada de observabilidade e monitoramento de uma
arquitetura Modern Data Stack (MDS), complementando ferramentas como OpenTelemetry e
OpenLineage, mas com um foco maior na visualização, alertas e armazenamento de dados
observáveis.

## Posicionamento no MDS

Na arquitetura MDS, a pilha Grafana atua principalmente nas seguintes áreas:

### Camada de Observabilidade e Monitoramento

- Fornece uma solução completa de observabilidade que cobre os "três pilares": métricas,
  logs e traces
- Serve como a interface visual e analítica para os dados coletados por instrumentação
  de sistemas
- Oferece capacidades de alerta que permitem identificação proativa de problemas

### Componentes específicos e suas funções:

**Grafana**:

- Interface principal para visualização e alertas
- Atua como o "front-end" para análise de todos os dados observáveis
- Permite a criação de dashboards customizados que podem exibir métricas de performance
  de pipelines, qualidade de dados e status de sistemas
- Na arquitetura MDS, conecta-se com várias fontes de dados para monitorar todo o fluxo
  de processamento

**Grafana Loki**:

- Sistema de agregação de logs multitenant
- No MDS, agrega logs de ferramentas de ETL/ELT, data warehouses, e outras ferramentas
  de processamento
- Permite correlacionar problemas nos dados com eventos registrados nos logs
- Usa um modelo de indexação eficiente que o torna mais adequado para grandes volumes de
  dados

**Grafana Tempo**:

- Backend de rastreamento distribuído de alta escala
- Complementa sistemas como OpenTelemetry na captura de traces
- No MDS, ajuda a acompanhar o fluxo de processamento de dados através de diferentes
  sistemas
- Facilita a identificação de gargalos e falhas em pipelines de dados

**Grafana Mimir**:

- Backend de métricas escalável e performático
- Armazena métricas de longo prazo para análise histórica e previsão
- No MDS, monitora performance de processamento, uso de recursos e SLAs de pipelines de
  dados
