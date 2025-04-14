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
import uuid
from icecream import ic
from prefect import flow, task
from prefect.cache_policies import TASK_SOURCE
from utils.client_factory import get_queue_client
from warehouse_objects import QueueMessage
import random

QUEUE_NAME = "foo"
MAX_ITEMS = 5
SECONDS_TO_WAIT = 30


@task(cache_policy=TASK_SOURCE)
def scan_collector_producer_task(queue_client, repo, status):
    ic(queue_client.send(QUEUE_NAME, {"repo": repo, "status": status}, sleep_seconds=SECONDS_TO_WAIT))


@task(retries=3, retry_delay_seconds=[1, 10, 30], cache_policy=TASK_SOURCE)
def scan_collector_consumer_pop_task(queue_client):
    """ Simula o processamento de QueueMessage """
    qm = queue_client.pop(QUEUE_NAME)
    if not qm:
        raise Exception("No Queue Message found")
    
    for key, value in qm.message.items():
        print(f"{key}: {value}")

    return True

@task
def scan_collector_consumer_read_archieve_task(queue_client):
    qmm_list = queue_client.read(QUEUE_NAME, sleep_seconds=SECONDS_TO_WAIT, limit=MAX_ITEMS)
    for qmm in qmm_list:
        print(f"{qmm.msg_id}: {qmm.message}")
        queue_client.archive(QUEUE_NAME, qmm.msg_id)


@flow(timeout_seconds=120)
def scan_collector_flow():
    queue_client = get_queue_client()

    # Cria entre 1 e 3 mensagens de eventos:
    for _ in range(1, random.randint(1, 3)):
        randon_repo_name = f"foo/{uuid.uuid4()}"  #randon generator
        scan_collector_producer_task(queue_client, randon_repo_name, "READ")
    
    scan_collector_consumer_pop_task(queue_client)


if __name__ == "__main__":
    scan_collector_flow()
