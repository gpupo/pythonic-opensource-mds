from typing import Any, Dict, Optional

from supabase import create_client as create_client_supabase

from .client import ClientContainer, ClientOptions
from .queue import QueueContainer


def create_client(
    url: str,
    key: str,
    options: Optional[ClientOptions | Dict[str, Any]] = None,
    target_class: Optional[type[ClientContainer]] = None,
) -> ClientContainer:
    """Creates and returns a configured client container.

    Args:
        url: The Supabase project URL
        key: The Supabase project API key
        options: Configuration options either as a ClientOptions instance or dict
        target_class: The class to instantiate (defaults to ClientContainer)

    """
    if not url:
        raise ValueError("URL cannot be empty")
    if not key:
        raise ValueError("Key cannot be empty")

    if options is not None and not isinstance(options, ClientOptions):
        options = create_options(options)
    if target_class is None:
        target_class = ClientContainer
    try:
        supabase_client = create_client_supabase(
            supabase_url=url, supabase_key=key, options=options
        )
        return target_class(supabase_client)
    except Exception as e:
        raise RuntimeError(f"Failed to create Supabase client: {str(e)}")


def create_options(schema: str = "public") -> ClientOptions:
    """Cria opcoes de configuracao para o client

    Args:
        schema (str, optional): schema do banco de dados. Defaults to "public".
         - pgmq_public para queue
    """
    return ClientOptions(schema=schema)


def create_queue_client(url: str, key: str):
    """Factory para CLient especializado em Filas"""
    return create_client(
        url=url,
        key=key,
        options=create_options("pgmq_public"),
        target_class=QueueContainer,
    )


__all__ = (
    "create_client",
    "create_queue_client",
    "create_options",
    "ClientContainer",
    "QueueContainer",
    "ClientOptions",
)
