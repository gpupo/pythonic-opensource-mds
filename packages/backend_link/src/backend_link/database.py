from typing import Any, Dict, List, Optional

from postgrest import (
    SyncRequestBuilder,
)
from warehouse_objects.sqlmodel import SQLModel

from backend_link.client import ClientContainer


class DatabaseContainer(ClientContainer):
    """Classe para acesso ao schema public via Rest."""

    def select_builder(
        self,
        model_class: SQLModel,
        request_builder: SyncRequestBuilder,
        args: Dict[str, Any],
    ) -> SyncRequestBuilder:
        """Monta o select com as condições de filtro"""

        # Define as colunas desejadas
        if args and "columns" in args:
            columns = args["columns"]
        else:
            columns = "*"
        request_builder = request_builder.select(columns)
        # if has revoked_at property
        if hasattr(model_class, "revoked_at"):
            request_builder = request_builder.neq("revoked_at", None)

        # Adiciona as condições de filtro
        if args and "filters" in args:
            for filter in args["filters"]:
                request_builder = request_builder.filter(filter)
        return request_builder

    def hydrate_one(
        self,
        model_class: SQLModel,
        data: Dict[str, Any],
        args: Optional[Dict[str, Any]] = None,
    ) -> SQLModel:
        """Executa o select de acordo com id e com as condições de filtro"""

        # obrigatorio id. TODO: implementar filtro por primary key
        if not data.get("id"):
            raise ValueError("id is required")

        request_builder: SyncRequestBuilder = self.client.table(model_class.__table__)
        request_builder = self.select_builder(model_class, request_builder, args)
        request_builder = request_builder.eq("id", data["id"])
        response = request_builder.execute()
        return model_class(**response.data[0])

    def hydrate_list(
        self, model_class: SQLModel, args: Optional[Dict[str, Any]] = {}
    ) -> List[SQLModel]:
        """Executa o select com as condições de filtro"""

        request_builder: SyncRequestBuilder = self.client.table(model_class.__table__)
        request_builder = self.select_builder(model_class, request_builder, args)
        # adiciona paginacao, custom ou default
        offset = args.get("offset", 0)
        limit = args.get("limit", 10)
        # Calcula o primeiro e ultimo item do range, exemplo 51-100
        page_item_start = offset
        page_item_end = offset + limit
        request_builder = request_builder.range(page_item_start, page_item_end)
        response = request_builder.execute()
        return [model_class(**d) for d in response.data]
