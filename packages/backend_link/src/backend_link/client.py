from supabase import Client as SupabaseClient
from supabase import ClientOptions as ClientOptionsSupabase


class ClientOptions(ClientOptionsSupabase):
    pass


class ClientContainer:
    """Classe base para uso de client Supabase ou substituto futuro

    Container para o client geralmente restful. Guarda o cliente em uma propriedade client
    e oferece os metodos de modo magico, entregando os metodos do client
    ou sobrecarregando metodos para adicionar funcionalidades

    Args:
        client (object): cliente restful

    """

    def __init__(self, client: SupabaseClient):
        self.client: SupabaseClient = client

    def __getattr__(self, name):
        return getattr(self.client, name)

    def rpc_execute(self, rpc_name: str, params: dict) -> dict:
        return self.client.rpc(
            rpc_name,
            params,
        ).execute()
