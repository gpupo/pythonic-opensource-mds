"""Testes para o client"""

import logging
from unittest.mock import MagicMock

import pytest
from backend_link import (
    DatabaseContainer,
)
from warehouse_objects.org import Org

logger = logging.getLogger(__name__)


@pytest.fixture
def database_container():
    mock_client = MagicMock()
    container = DatabaseContainer(client=mock_client)
    return container


class TestClient:
    def test_hydrate_one(self, database_container):
        # Mocks
        mock_request_builder = MagicMock()
        mock_response = MagicMock()
        mock_response.data = [
            {
                "id": "1",
                "login": "test",
                "name": "test",
                "url": "test",
                "image": "test",
                "description": "test",
                "is_public": True,
                "revoked_at": None,
            }
        ]

        # Encadeamento dos métodos
        mock_request_builder.select.return_value = mock_request_builder
        mock_request_builder.neq.return_value = mock_request_builder
        mock_request_builder.eq.return_value = mock_request_builder
        mock_request_builder.execute.return_value = mock_response

        database_container.client.table.return_value = mock_request_builder

        # Executa método real
        org = database_container.hydrate_one(Org, {"id": 1}, {"columns": "*"})

        assert isinstance(org, Org)
        assert org.id == "1"
        assert org.login == "test"
        assert org.name == "test"
        assert org.url == "test"
        assert org.image == "test"
        assert org.description == "test"
        assert org.is_public is True
        assert org.revoked_at is None

    def test_hydrate_list(self, database_container):
        mock_request_builder = MagicMock()
        mock_response = MagicMock()
        mock_response.data = [
            {
                "id": "1",
                "login": "test",
                "name": "test",
                "url": "test",
                "image": "test",
                "description": "test",
                "is_public": True,
                "revoked_at": None,
            },
            {
                "id": "2",
                "login": "test2",
                "name": "test2",
                "url": "test2",
                "image": "test2",
                "description": "test2",
                "is_public": False,
                "revoked_at": None,
            },
        ]

        # Encadeamento dos métodos
        mock_request_builder.select.return_value = mock_request_builder
        mock_request_builder.neq.return_value = mock_request_builder
        mock_request_builder.range.return_value = mock_request_builder
        mock_request_builder.execute.return_value = mock_response

        database_container.client.table.return_value = mock_request_builder

        # Executa método real
        orgs = database_container.hydrate_list(Org, {"offset": 0, "limit": 10})

        assert isinstance(orgs, list)
        assert len(orgs) == 2
        assert orgs[0].id == "1"
        assert orgs[1].id == "2"
