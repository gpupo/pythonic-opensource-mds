import os

from backend_link import create_queue_client
from infra_env import env

# Verifique se o ambiente está configurado
if not env.is_running_in_container():
    if not env.load_env():
        raise RuntimeError("Could not load .env file for configuration")

API_EXTERNAL_URL = os.environ["API_EXTERNAL_URL"]
SERVICE_ROLE_KEY = os.environ["SERVICE_ROLE_KEY"]

# Criação do objeto QueueContainer
_queue_client = create_queue_client(url=API_EXTERNAL_URL, key=SERVICE_ROLE_KEY)


def get_queue_client():
    """Retorna a instância compartilhada de QueueContainer."""
    return _queue_client
