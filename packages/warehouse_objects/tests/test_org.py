import unittest
from datetime import datetime
from unittest.mock import MagicMock
from uuid import uuid4

from warehouse_objects.sqlmodel import Session
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

class TestTag(unittest.TestCase):
    def test_tag_initialization(self):
        tag = Tag(type="Y", year=2025, number=1)
        self.assertEqual(tag.id, "2025_Y")


class TestTagCollection(unittest.TestCase):
    def test_find_by_type_and_timerange(self):
        session = MagicMock()
        collection = TagCollection(session)
        collection.find_by_type_and_timerange(
            "test", datetime(2025, 1, 1), datetime(2025, 12, 31)
        )
        session.query.assert_called()


class TestOrg(unittest.TestCase):
    def test_org_creation(self):
        org = Org(id=1, login="example", name="Example Org", is_public=True)
        self.assertEqual(org.login, "example")


class TestProfileOrgLink(unittest.TestCase):
    def test_profile_org_link(self):
        link = ProfileOrgLink(profile_id=uuid4(), org_id=1)
        self.assertIsNotNone(link.profile_id)


class TestUser(unittest.TestCase):
    def test_user_creation(self):
        user = User(id=1, username="testuser", email="test@example.com", role="admin")
        self.assertEqual(user.username, "testuser")


class TestRepositoryConfig(unittest.TestCase):
    def test_get_config(self):
        session = MagicMock()
        default_config = DefaultConfig(name="test_key", value={"key": "value"})
        session.query.return_value.filter.return_value.first.return_value = (
            default_config
        )

        config = RepositoryConfig(spec={"test_key": "value"})
        value = config.get_config("test_key", session)
        self.assertEqual(value, "value")

    def test_set_config(self):
        config = RepositoryConfig()
        config.set_config("test_key", "value")
        self.assertEqual(config.spec["test_key"], "value")


if __name__ == "__main__":
    unittest.main()
