from supabase import ClientOptions as ClientOptionsSupabase

from backend_link.client import ClientContainer


class ClientOptions(ClientOptionsSupabase):
    pass


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
