""" Testes para o client """

import unittest

from backend_link.client import create_client, create_options
from supabase import AsyncClientOptions, Client as SupabaseClient
from backend_link.client import ClientContainer

class TestClient(unittest.TestCase):
    def test_create_options(self):
        options = create_options()
        self.assertEqual(options.schema, "public")

    def test_create_client(self):
        client = create_client()
        self.assertIsInstance(client, ClientContainer) 
        self.assertIsInstance(client.client, SupabaseClient)
