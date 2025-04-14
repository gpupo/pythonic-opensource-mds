from backend_link.client import ClientContainer


class QueueContainer(ClientContainer):
    """Classe para acesso ao pgmq via Rest.

    send - Envia uma mensagem para a fila
    sendBatch - Envia múltiplas mensagens de uma vez
    read - Lê mensagens sem removê-las da fila
    pop - Recupera e remove a próxima mensagem disponível
    archive - Move uma mensagem para a tabela de arquivo
    delete - Exclui permanentemente uma mensagem
    """

    def send(self, queue_name: str, message: dict, sleep_seconds: int = 0) -> dict:
        """Envia uma mensagem para a fila"""
        response = self.rpc_execute(
            "send",
            {
                "queue_name": queue_name,
                "message": message,
                "sleep_seconds": sleep_seconds,
            },
        )

        if not response.data:
            raise Exception("Failed to send message to queue")

        return response.data

    def sendBatch(
        self, queue_name: str, messages: list, sleep_seconds: int = 0
    ) -> dict:
        """Envia múltiplas mensagens de uma vez"""
        response = self.rpc_execute(
            "sendBatch",
            {
                "queue_name": queue_name,
                "messages": messages,
                "sleep_seconds": sleep_seconds,
            },
        )

        if not response.data:
            raise Exception("Failed to send batch messages to queue")

        return response.data

    def read(self, queue_name: str, sleep_seconds: int = 0, limit: int = 10) -> list:
        """Lê mensagens sem removê-las da fila

        queue_name (text): Queue name
        sleep_seconds (integer): Visibility timeout in seconds
        n (integer): Maximum number of Messages to read
        """
        response = self.rpc_execute(
            "read",
            {"queue_name": queue_name, "sleep_seconds": sleep_seconds, "n": limit},
        )

        if not response.data:
            raise Exception("Failed to read messages from queue")

        return response.data

    def pop(self, queue_name: str) -> dict:
        """Recupera e remove a próxima mensagem disponível"""
        response = self.rpc_execute(
            "pop",
            {"queue_name": queue_name},
        )

        if not response.data:
            raise Exception("Failed to pop message from queue")

        return response.data

    def archive(self, queue_name: str, message_id: int) -> dict:
        """Move uma mensagem para a tabela de arquivo"""
        response = self.rpc_execute(
            "archive",
            {"queue_name": queue_name, "message_id": message_id},
        )

        if not response.data:
            raise Exception("Failed to archive message in queue")

        return response.data

    def delete(self, queue_name: str, message_id: int) -> dict:
        """Exclui permanentemente uma mensagem"""
        response = self.rpc_execute(
            "delete",
            {"queue_name": queue_name, "message_id": message_id},
        )

        if not response.data:
            raise Exception("Failed to delete message from queue")

        return response.data
