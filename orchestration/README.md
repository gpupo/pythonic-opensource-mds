[Prefect doc](https://docs.prefect.io/)

Verificar o setup

    uv run prefect version

local API serve

    uv run prefect server start &

Rodar localmente um flow

    uv run flows/{nome}_flow.py

## Estrutura

A pasta utils seria dedicada a utilitários e fábricas que são usados em várias partes do
projeto.

# Conceitos

A diferença entre **orquestração** e **coreografia** está no **controle** e na
**coordenação** das interações entre serviços em uma arquitetura distribuída (como
microservices ou Event-Driven Architecture):

## **1. Orquestração**

- **Um componente central (orquestrador)** controla o fluxo.
- Ele **chama explicitamente** cada serviço participante na ordem desejada.
- Os serviços são **passivos**, respondendo às instruções.

### Exemplo:

Um **orquestrador (ex: Prefect, Apache Airflow)** executa uma tarefa:

1. Chama o serviço A
2. Quando termina, chama o serviço B
3. Depois, chama o serviço C

### Analogia:

Maestro regendo uma orquestra — cada músico toca quando o maestro manda.

## **2. Coreografia**

- **Não há controle central**.
- Cada serviço **age de forma autônoma**, reagindo a eventos.
- A comunicação é **indireta**, via **eventos publicados** e **assinados** (ex: Kafka,
  NATS, RabbitMQ).

### Exemplo:

1. Serviço A publica um evento `PedidoCriado`
2. Serviço B escuta e reage (`ReservaEstoque`)
3. Serviço C escuta e reage (`EmitirNotaFiscal`)

### Analogia:

Uma dança onde cada dançarino sabe seu papel e reage aos movimentos dos outros — sem um
coreógrafo presente no momento da execução.
