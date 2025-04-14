"""
Exemplo de uso de [Event-driven architecture](https://en.wikipedia.org/wiki/Event-driven_architecture) em conjunto com o queue_client

- Event Producer task = scan_collector_producer_task;
- Event Consumer task = scan_collector_consumer_task;
- Simple event processing flow = scan_collector_flow

NOTE: Criar fila, adicione migration:
select from pgmq.create('foo');

NOTE: Listart as filas
select * from pgmq.list_queues();

"""

import asyncio

from icecream import ic
from prefect import flow, pause_flow_run, task
from prefect.cache_policies import TASK_SOURCE
from utils.client_factory import get_queue_client

QUEUE_NAME = "foo"
MAX_ITEMS = 5
SECONDS_TO_WAIT = 30


@task(cache_policy=TASK_SOURCE)
async def scan_collector_producer_task(queue_client):
    ic(queue_client.send(QUEUE_NAME, {"repo": "org/app", "status": "ok"}))


@task(cache_policy=TASK_SOURCE)
async def scan_collector_consumer_task(queue_client):
    event = queue_client.pop(QUEUE_NAME)
    if event:
        ic(event)
        return True


def list_events(queue_client):
    print("Listagem de ate 5 eventos na fila, inseridos a mais de 30 segundos")
    ic(queue_client.read(QUEUE_NAME, sleep_seconds=SECONDS_TO_WAIT, limit=MAX_ITEMS))


@flow
async def scan_collector_flow():
    queue_client = get_queue_client()
    scan_collector_producer_task(queue_client)
    list_events(queue_client)
    await pause_flow_run(timeout=SECONDS_TO_WAIT)
    list_events(queue_client)
    while scan_collector_consumer_task(queue_client) is True:
        scan_collector_consumer_task(queue_client)


if __name__ == "__main__":
    asyncio.run(scan_collector_flow())
