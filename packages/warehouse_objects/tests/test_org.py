import unittest
from datetime import datetime
from unittest.mock import patch

from warehouse_objects import Org, Product, Repository, RepositoryTag, Tag


class TestOrg(unittest.TestCase):
    def setUp(self):
        self.org = Org(
            name="TestOrg",
            url="http://test.org",
            image="test.jpg",
            products=[
                Product(
                    name="TestProduct",
                    repositories=[
                        Repository(
                            name="TestRepo",
                            description="TestRepoDescription",
                            url="http://test.repo",
                            branch_production="main",
                            tags=[
                                RepositoryTag(
                                    id="TestTag",
                                    sha1="sha1",
                                    type="Y",
                                    start_date="2024-01-01T00:00:00",
                                    end_date="2024-12-31T23:59:59",
                                )
                            ],
                        )
                    ],
                )
            ],
        )

    def test_org_name(self):
        self.assertEqual(self.org.name, "TestOrg")

    def test_org_url(self):
        self.assertEqual(self.org.url, "http://test.org")

    def test_org_image(self):
        self.assertEqual(self.org.image, "test.jpg")

    def test_product_name(self):
        self.assertEqual(self.org.products[0].name, "TestProduct")

    def test_repository_name(self):
        self.assertEqual(self.org.products[0].repositories[0].name, "TestRepo")

    def test_repository_description(self):
        self.assertEqual(
            self.org.products[0].repositories[0].description, "TestRepoDescription"
        )

    def test_repository_url(self):
        self.assertEqual(self.org.products[0].repositories[0].url, "http://test.repo")

    def test_repository_branch_production(self):
        self.assertEqual(self.org.products[0].repositories[0].branch_production, "main")

    def test_repository_tag(self):
        tag = self.org.products[0].repositories[0].tags[0]
        self.assertEqual(tag.id, "TestTag")
        self.assertEqual(tag.type, "Y")
        # test if the strings start_date and end_date are in datetime strlen
        self.assertEqual(len(tag.start_date), 19)
        self.assertEqual(len(tag.end_date), 19)
