import os

from backend_link import (
    DatabaseContainer,
    QueueContainer,
    create_database_client,
    create_queue_client,
)
from infra_env import env

# Verifica uma unica vez se o ambiente está configurado
if not hasattr(env, "_initialized"):
    if not env.is_running_in_container():
        if not env.load_env():
            raise RuntimeError("Could not load .env file for configuration")

    env._initialized = True

API_EXTERNAL_URL = os.environ["API_EXTERNAL_URL"]
SERVICE_ROLE_KEY = os.environ["SERVICE_ROLE_KEY"]


def get_database_client() -> DatabaseContainer:
    """Cria e retorna uma instância de DatabaseContainer."""
    return create_database_client(url=API_EXTERNAL_URL, key=SERVICE_ROLE_KEY)


def get_queue_client() -> QueueContainer:
    """Cria e retorna uma instância de QueueContainer."""
    return create_queue_client(url=API_EXTERNAL_URL, key=SERVICE_ROLE_KEY)


__all__ = ["get_database_client", "get_queue_client"]

