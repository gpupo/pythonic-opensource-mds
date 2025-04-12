""" Testes para o client """

import unittest

from infra_env import env
from backend_link import create_client, create_options, create_queue_client
from backend_link import ClientContainer
from backend_link import QueueContainer

import os
# Load environment variables if not running in a container
if not env.is_running_in_container():
    if not env.load_env():
        raise RuntimeError("Could not load .env file for configuration")


API_EXTERNAL_URL = os.environ["API_EXTERNAL_URL"]
SERVICE_ROLE_KEY = os.environ["SERVICE_ROLE_KEY"]

class TestClient(unittest.TestCase):



    def test_create_options(self):
        options = create_options(schema="foo")
        self.assertEqual(options.schema, "foo")

    def test_create_client(self):
        client = create_client(url=API_EXTERNAL_URL, key=SERVICE_ROLE_KEY)
        self.assertIsInstance(client, ClientContainer) 
     
    def test_create_queue_client(self):
        client = create_queue_client(url = API_EXTERNAL_URL, key=SERVICE_ROLE_KEY)
        self.assertIsInstance(client, QueueContainer) 