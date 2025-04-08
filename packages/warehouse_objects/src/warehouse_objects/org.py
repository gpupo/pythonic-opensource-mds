from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class Tag(SQLModel, table=True):
    id: str = Field(primary_key=True)
    type: str
    start_date: datetime = None
    end_date: datetime = None
    year: int
    number: int

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.type == "Y":
            self.id = f"{self.year}_{self.type}"
        else:
            self.id = f"{self.year}_{self.type}_{self.number}"


class TagCollection:
    def __init__(self, session):
        self.session = session

    def find_by_type_and_timerange(
        self, type: str, start_datetime: datetime, end_datetime: datetime
    ):
        marks = (
            self.session.query(Tag)
            .where(Tag.type == type)
            .where(
                Tag.start_date >= start_datetime,
                Tag.end_date <= end_datetime,
            )
            .all()
        )
        return marks


class Org(SQLModel, table=True):
    """Classe Org que representa uma organização"""

    id: int | None = Field(default=None, primary_key=True)
    login: str
    name: str
    url: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None
    products: list["Product"] = Relationship(back_populates="org")


class Product(SQLModel, table=True):
    """Classe Product que representa um produto"""

    id: int | None = Field(default=None, primary_key=True)
    org_id: int = Field(foreign_key="org.id")
    name: str
    description: Optional[str] = None
    org: Org = Relationship(back_populates="products")
    repositories: list["Repository"] = Relationship(back_populates="product")


class Repository(SQLModel, table=True):
    """Representa um repo git de um componente do produto"""

    id: int | None = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")
    name: str
    description: Optional[str] = None
    url: Optional[str] = None
    branch_production: Optional[str] = None
    product: Product = Relationship(back_populates="repositories")
    tags: list["RepositoryTag"] = Relationship(back_populates="repository")


class RepositoryTag(SQLModel, table=True):
    """
    Armazena o sha1 do commit do Repository para cada
    Tag existente.

    Exemplo: 2024_S_1,sha12...
    """

    id: str = Field(primary_key=True)
    type: str
    start_date: datetime = None
    end_date: datetime = None
    repository_id: int = Field(foreign_key="repository.id")
    sha1: str
    repository: Repository = Relationship(back_populates="tags")
