import unittest
from datetime import datetime
from unittest.mock import MagicMock
from uuid import uuid4

from sqlmodel import Session
from warehouse_objects.org import (
    DefaultConfig,
    Field,
    Org,
    Product,
    Profile,
    ProfileOrgLink,
    Repository,
    RepositoryConfig,
    RepositoryTag,
    Tag,
    TagCollection,
    User,
)


class TestField(unittest.TestCase):
    def test_field_without_description(self):
        """Testa o Field sem a descrição"""
        field = Field(primary_key=True)
        self.assertIsNotNone(field)

    def test_field_with_description(self):
        """Testa o Field com a descrição."""
        field = Field(primary_key=True, description="Um campo de teste")
        self.assertIsNotNone(field)
        # Verifica se 'sa_column_kwargs' contém o comentário
        self.assertIn("comment", field.sa_column_kwargs)
        self.assertEqual(field.sa_column_kwargs["comment"], "Um campo de teste")

