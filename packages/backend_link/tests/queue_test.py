from datetime import datetime
from unittest.mock import MagicMock

import pytest
from backend_link.queue import QueueContainer, _factory_queue_message
from warehouse_objects import QueueMessage


@pytest.fixture
def queue_container():
    mock_client = MagicMock()
    container = QueueContainer(client=mock_client)
    container.rpc_execute = MagicMock()
    return container


# Constantes para os testes
TEST_QUEUE = "test_queue"
TEST_MESSAGE = {"foo": "bar1"}
TEST_MESSAGE_ID = 123
TEST_RESPONSE = {
    "msg_id": TEST_MESSAGE_ID,
    "read_ct": 1,
    "vt": "2023-08-16 08:38:29.989841-05",
    "message": TEST_MESSAGE,
    "enqueued_at": "2023-08-16 08:37:54.567283-05",
}


class TestQueueOperations:
    def test_send(self, queue_container):
        """Testa o envio de mensagem com e sem sleep"""
        # Configuração
        queue_container.rpc_execute.return_value.data = TEST_RESPONSE

        # Teste básico
        result = queue_container.send(TEST_QUEUE, TEST_MESSAGE)

        # Verificações
        queue_container.rpc_execute.assert_called_with(
            "send",
            {"queue_name": TEST_QUEUE, "message": TEST_MESSAGE, "sleep_seconds": 0},
        )
        assert result == TEST_RESPONSE

    def test_send_failure(self, queue_container):
        """Testa falha no envio da mensagem"""
        queue_container.rpc_execute.return_value.data = None

        with pytest.raises(Exception, match="Failed to send message to queue"):
            queue_container.send(TEST_QUEUE, TEST_MESSAGE)

    def test_read(self, queue_container):
        """Testa leitura de mensagens com diversos parâmetros"""
        # Simula sucesso com múltiplas mensagens
        queue_container.rpc_execute.return_value.data = [TEST_RESPONSE, TEST_RESPONSE]

        result = queue_container.read(TEST_QUEUE)

        # Verificações
        queue_container.rpc_execute.assert_called_with(
            "read", {"queue_name": TEST_QUEUE, "sleep_seconds": 0, "n": 10}
        )
        assert len(result) == 2
        assert all(isinstance(msg, QueueMessage) for msg in result)

    def test_read_empty(self, queue_container):
        """Testa leitura de fila vazia"""
        queue_container.rpc_execute.return_value.data = None
        result = queue_container.read(TEST_QUEUE)
        assert result == []

    def test_pop(self, queue_container):
        """Testa remoção e leitura de mensagem da fila"""
        # Simula sucesso
        queue_container.rpc_execute.return_value.data = [TEST_RESPONSE]

        result = queue_container.pop(TEST_QUEUE)

        # Verificações
        queue_container.rpc_execute.assert_called_with(
            "pop", {"queue_name": TEST_QUEUE}
        )
        assert isinstance(result, QueueMessage)
        assert result.msg_id == TEST_MESSAGE_ID

        # Simula fila vazia
        queue_container.rpc_execute.reset_mock()
        queue_container.rpc_execute.return_value.data = None
        result = queue_container.pop(TEST_QUEUE)
        assert result is None


def test_queue_message_factory():
    """Testa função de criação de mensagem de fila"""
    # Esta função depende da implementação real de _factory_queue_message
    # Supondo que ela exista no módulo importado

    message = _factory_queue_message("test_queue", TEST_RESPONSE)

    assert isinstance(message, QueueMessage)
    assert message.msg_id == TEST_MESSAGE_ID
    message.queue_name == "test_queue"
    assert message.message == {"foo": "bar1"}
