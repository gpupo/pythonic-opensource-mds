# [PGMQ](https://github.com/tembo-io/pgmq) (PostgreSQL Message Queue)

solução de filas de mensagens implementada diretamente no PostgreSQL. Esta documentação
sintetiza as principais funções disponíveis no esquema `pgmq_public`.

## Funções Principais

### Gerenciamento de Mensagens

#### `pgmq_public.pop(queue_name)`

Recupera a próxima mensagem disponível e a remove da fila especificada.

- `queue_name` (`text`): Nome da fila

#### `pgmq_public.send(queue_name, message, sleep_seconds)`

Adiciona uma mensagem à fila especificada, opcionalmente atrasando sua visibilidade.

- `queue_name` (`text`): Nome da fila
- `message` (`jsonb`): Payload da mensagem a ser enviada
- `sleep_seconds` (`integer`, opcional): Atrasa a visibilidade da mensagem pelo número
  de segundos especificado. Padrão: 0

#### `pgmq_public.send_batch(queue_name, messages, sleep_seconds)`

Adiciona um lote de mensagens à fila especificada, com atraso opcional.

- `queue_name` (`text`): Nome da fila
- `messages` (`jsonb[]`): Array de payloads de mensagens a serem enviadas
- `sleep_seconds` (`integer`, opcional): Atrasa a visibilidade das mensagens pelo número
  de segundos especificado. Padrão: 0

#### `pgmq_public.archive(queue_name, message_id)`

Arquiva uma mensagem movendo-a da tabela da fila para a tabela de arquivo da fila.

- `queue_name` (`text`): Nome da fila
- `message_id` (`bigint`): ID da mensagem a ser arquivada

#### `pgmq_public.delete(queue_name, message_id)`

Exclui permanentemente uma mensagem da fila especificada.

- `queue_name` (`text`): Nome da fila
- `message_id` (`bigint`): ID da mensagem a ser excluída

#### `pgmq_public.read(queue_name, sleep_seconds, n)`

Lê até "n" mensagens da fila especificada com um tempo de visibilidade opcional.

- `queue_name` (`text`): Nome da fila
- `sleep_seconds` (`integer`): Tempo de visibilidade em segundos
- `message_id` (`integer`): Número máximo de mensagens a serem lidas

## Exemplo de Uso com Supabase (Python)

```python
import asyncio

from supabase import AsyncClientOptions, create_client

# ....

# Configuração do cliente
options = AsyncClientOptions(schema="pgmq_public")
supabase = create_client(url, key, options=options)

# Função para enviar eventos para uma fila
async def send_event(queue_name: str, evento: str, payload: dict):
    response = await supabase.postgrest.rpc(
        "send",
        {
            "queue_name": queue_name,
            "message": {"evento": evento, "payload": payload},
            "sleep_seconds": 0,
        },
    ).execute()

    if response.data:
        print(f"[{queue_name.upper()}] Mensagem enviada:", response.data)
    else:
        print(f"[{queue_name.upper()}] Erro:", response.error)
```
