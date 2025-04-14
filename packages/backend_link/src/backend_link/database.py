
from warehouse_objects.org import *
from backend_link.client import ClientContainer


class DatabaseContainer(ClientContainer):
    """Classe para acesso ao pgmq via Rest.

    data =  database_client.table("org").select("name").execute()
    list = database_client.hydrate(Org, data)
    """
    def hydrate(self, target_class: type["SQLModel"], data: dict) -> list["SQLModel"]:
        return [target_class(data) for data in data]