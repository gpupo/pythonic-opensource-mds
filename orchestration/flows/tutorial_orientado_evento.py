import os

from backend_link import (
    ClientContainer,
    QueueContainer,
    create_client,
    create_options,
    create_queue_client,
)
from icecream import ic
from infra_env import env

# Load environment variables if not running in a container
if not env.is_running_in_container():
    if not env.load_env():
        raise RuntimeError("Could not load .env file for configuration")


API_EXTERNAL_URL = os.environ["API_EXTERNAL_URL"]
SERVICE_ROLE_KEY = os.environ["SERVICE_ROLE_KEY"]

queue_client: QueueContainer = create_queue_client(
    url=API_EXTERNAL_URL, key=SERVICE_ROLE_KEY
)
# send, send_batch, read, pop, archive, delete

# NOTE: Criar fila, adicione migration:
# select from pgmq.create('foo');

ic(queue_client.send("foo", {"repo": "org/app", "status": "ok"}))
ic(queue_client.read("foo", sleep_seconds=0, limit=5))
ic(queue_client.pop("foo"))
