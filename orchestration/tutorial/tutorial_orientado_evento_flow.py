"""
Exemplo de uso de [Event-driven architecture](https://en.wikipedia.org/wiki/Event-driven_architecture) em conjunto com o queue_client

- Event Producer task = scan_collector_producer_task;
- Event Consumer = scan_collector_consumer_pop_task;
- Simple event processing flow = scan_collector_flow

NOTE: Criar fila, adicione migration:
select from pgmq.create('foo');

NOTE: Listart as filas
select * from pgmq.list_queues();

"""

import random
import uuid

from icecream import ic
from prefect import flow, task
from prefect.cache_policies import INPUTS, NO_CACHE, RUN_ID
from prefect.logging import get_run_logger
from tabulate import tabulate
from utils.client_factory import get_queue_client
from warehouse_objects import QueueMessage

QUEUE_NAME = "foo"
MAX_ITEMS = 5
SECONDS_TO_WAIT = 0


@task(cache_policy=NO_CACHE, tags=["tutorial"])
def scan_collector_producer_task(queue_client, repo_name, status):
    print("Simula tarefa geradora de eventos")
    response = queue_client.send(
        QUEUE_NAME,
        {"repo": repo_name, "status": status},
        sleep_seconds=SECONDS_TO_WAIT,
    )
    print(response)
    print(f"Produced message on {QUEUE_NAME} for repo: {repo_name}")


@task(
    retries=3, retry_delay_seconds=[1, 5, 10], cache_policy=NO_CACHE, tags=["tutorial"]
)
def scan_collector_consumer_pop_task(queue_client):
    """Simula o processamento de QueueMessage"""
    qm: QueueMessage = queue_client.pop(QUEUE_NAME)
    if not qm:
        raise Exception("No Queue Message found")

    print(tabulate(qm, tablefmt="plain"))
    print("Fazendo algo com a mensagem removida da fila... ")

    return True


@task(cache_policy=NO_CACHE, tags=["tutorial"])
def scan_collector_consumer_read_archieve_task(queue_client):
    qm_list = queue_client.read(
        QUEUE_NAME, sleep_seconds=SECONDS_TO_WAIT, limit=MAX_ITEMS
    )
    for qm in qm_list:
        print(tabulate(qm, tablefmt="plain"))
        print("Fazendo algo com a mensagem ainda na fila... ")
        ic(queue_client.archive(qm))  # arquiva


@flow(timeout_seconds=120, log_prints=True)
def scan_collector_flow():
    logger = get_run_logger()
    """Simula um flow com eventos usando pgmq via supabase"""
    queue_client = get_queue_client()
    for _ in range(3):
        random_repo_name = f"foo/{uuid.uuid4().hex}"  # Using hex for shorter IDs
        print(f"{random_repo_name}")
        scan_collector_producer_task(queue_client, random_repo_name, "READ")

    scan_collector_consumer_pop_task(queue_client)
    scan_collector_consumer_read_archieve_task(queue_client)
    logger.info("Flow completed successfully")


if __name__ == "__main__":
    scan_collector_flow()
