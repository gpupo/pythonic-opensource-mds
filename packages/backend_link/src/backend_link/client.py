import os
from typing import Optional
from supabase import AsyncClientOptions, Client as SupabaseClient, create_client as create_client_supabase
from infra_env import env

# Load environment variables if not running in a container
if not env.is_running_in_container():
    if not env.load_env():
        raise RuntimeError("Could not load .env file for configuration")


API_EXTERNAL_URL = os.environ["API_EXTERNAL_URL"]
SERVICE_ROLE_KEY = os.environ["SERVICE_ROLE_KEY"]

def create_options(schema:str="public") -> AsyncClientOptions:
    """ Cria opcoes de configuracao para o client 
    
    Args:
        schema (str, optional): schema do banco de dados. Defaults to "public".
         - pgmq_public para queue
    """
    return AsyncClientOptions(schema=schema)

class ClientContainer:
    """ Classe base para uso de client Supabase ou substituto futuro
    
    Container para o client geralmente restful. Guarda o cliente em uma propriedade client 
    e oferece os metodos de modo magico, entregando os metodos do client
    ou sobrecarregando metodos para adicionar funcionalidades

    Args:
        client (object): cliente restful

    """

    def __init__(self, client:SupabaseClient):
        self.client: SupabaseClient = client

    def __getattr__(self, name):
        return getattr(self.client, name)

    
def create_client(url=API_EXTERNAL_URL, key=SERVICE_ROLE_KEY, options:Optional[AsyncClientOptions]=None):
    return ClientContainer(create_client_supabase(supabase_url=url, supabase_key=key, options=options))
