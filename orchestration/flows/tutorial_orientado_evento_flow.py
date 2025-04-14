from icecream import ic
from utils.client_factory import get_queue_client

queue_client = get_queue_client()

# NOTE: Criar fila, adicione migration:
# select from pgmq.create('foo');
# select * from pgmq.list_queues(); #list


ic(queue_client.send("foo", {"repo": "org/app", "status": "ok"}))
ic(queue_client.read("foo", sleep_seconds=0, limit=5))
ic(queue_client.pop("foo"))
