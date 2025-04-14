import unittest
from unittest.mock import MagicMock

from backend_link.queue import QueueContainer


class TestQueueContainer(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock()
        self.queue = QueueContainer(client=self.mock_client)
        self.queue.rpc_execute = MagicMock()

    def test_sendBatch(self):
        self.queue.rpc_execute.return_value = MagicMock(data={"result": "success"})
        messages = [{"key1": "value1"}, {"key2": "value2"}]
        response = self.queue.sendBatch("test_queue", messages, sleep_seconds=2)
        self.queue.rpc_execute.assert_called_with(
            "sendBatch",
            {
                "queue_name": "test_queue",
                "messages": messages,
                "sleep_seconds": 2,
            },
        )
        self.assertEqual(response, {"result": "success"})


if __name__ == "__main__":
    unittest.main()
