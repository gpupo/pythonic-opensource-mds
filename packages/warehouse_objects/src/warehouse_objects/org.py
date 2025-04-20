import uuid
from datetime import datetime
from typing import Any, List, Optional
from warehouse_objects.sqlmodel import Field,  SQLModel, JSON, Column, Relationship

class Tag(SQLModel, table=True):
    """Tabela que armazena tags associadas a repositórios."""

    __table_args__ = {"comment": "Tabela de tags do sistema"}

    id: str = Field(primary_key=True, description="Identificador único da tag.")
    type: str = Field(description="Tipo da tag.")
    start_date: datetime = Field(default=None, description="Data de início da tag.")
    end_date: datetime = Field(default=None, description="Data de término da tag.")
    year: int = Field(description="Ano associado à tag.")
    number: int = Field(description="Número associado à tag.")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.type == "Y":
            self.id = f"{self.year}_{self.type}"
        else:
            self.id = f"{self.year}_{self.type}_{self.number}"


class TagCollection:
    """Classe para manipulação de coleções de tags."""

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


class ProfileOrgLink(SQLModel, table=True):
    """Tabela de associação."""

    __table_args__ = {"comment": "Table pivot"}

    profile_id: uuid.UUID = Field(
        foreign_key="profile.id", primary_key=True, description="ID do perfil"
    )
    org_id: int = Field(
        foreign_key="org.id", primary_key=True, description="ID da organização"
    )


class Org(SQLModel, table=True):
    """Organization."""

    __table_args__ = {"comment": "Tabela que representa uma organização."}

    id: int | None = Field(
        default=None, primary_key=True, description="ID único da organização."
    )
    login: str = Field(description="Login da organização.")
    name: str = Field(description="Nome da organização.")
    url: Optional[str] = Field(default=None, description="URL associada à organização.")
    image: Optional[str] = Field(
        default=None, description="Imagem representativa da organização."
    )
    description: Optional[str] = Field(
        default=None, description="Descrição da organização."
    )
    is_public: bool = Field(
        default=False, description="Define se a visibilidade é pública."
    )
    revoked_at: Optional[datetime] = Field(
        default=None, description="Data de revogação da organização."
    )
    products: List["Product"] = Relationship(back_populates="org")
    profiles: List["Profile"] = Relationship(
        back_populates="orgs", link_model=ProfileOrgLink
    )


class User(SQLModel, table=True):
    """Representa tabela maior do schema auth."""

    __tablename__ = "users"
    __table_args__ = {"schema": "auth"}

    id: int = Field(primary_key=True, description="ID do usuário")
    username: str = Field(description="Nome do usuário")
    email: str = Field(description="E-mail do usuário")
    role: str = Field(description="Papel")


class Profile(SQLModel, table=True):
    """Tabela atualizada por trigger no login.
    INFO: https://supabase.com/docs/guides/auth/managing-user-data
    """

    __table_args__ = {"comment": "Perfil de usuarios"}

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="auth.users.id")
    name: Optional[str] = None
    orgs: List[Org] = Relationship(back_populates="profiles", link_model=ProfileOrgLink)


class Product(SQLModel, table=True):
    """Tabela que representa um produto."""

    __table_args__ = {"comment": "Produto de Software que aninha componentes"}

    id: int | None = Field(
        default=None, primary_key=True, description="ID único do produto."
    )
    org_id: int = Field(
        foreign_key="org.id", description="ID da organização associada ao produto."
    )
    name: str = Field(description="Nome do produto.")
    description: Optional[str] = Field(
        default=None, description="Descrição do produto."
    )
    is_public: bool = Field(
        default=False, description="Define se a visibilidade é pública."
    )
    revoked_at: Optional[datetime] = Field(
        default=None, description="Data de revogação do produto."
    )
    org: Org = Relationship(back_populates="products")
    repositories: List["Repository"] = Relationship(back_populates="product")


class Repository(SQLModel, table=True):
    """Tabela que representa um repositório git de um componente do produto."""

    __table_args__ = {"comment": "Repo Git-Based de um componente"}

    id: int | None = Field(
        default=None, primary_key=True, description="ID único do repositório."
    )
    product_id: int = Field(
        foreign_key="product.id", description="ID do produto associado ao repositório."
    )
    name: str = Field(description="Nome do repositório.")
    description: Optional[str] = Field(
        default=None, description="Descrição do repositório."
    )
    url: Optional[str] = Field(default=None, description="URL do repositório.")
    is_public: bool = Field(
        default=False, description="Define se a visibilidade é pública."
    )
    branch_production: Optional[str] = Field(
        default=None, description="Branch de produção do repositório."
    )
    product: Product = Relationship(back_populates="repositories")
    tags: List["RepositoryTag"] = Relationship(back_populates="repository")
    configs: List["RepositoryConfig"] = Relationship(back_populates="repository")


class RepositoryTag(SQLModel, table=True):
    """Tabela que armazena o SHA1 do commit do repositório para cada tag existente."""

    __table_args__ = {"comment": "Tags sobre commits do repo git-based"}

    id: str = Field(
        primary_key=True, description="Identificador único da tag do repositório."
    )
    type: str = Field(description="Tipo da tag.")
    start_date: datetime = Field(default=None, description="Data de início da tag.")
    end_date: datetime = Field(default=None, description="Data de término da tag.")
    repository_id: int = Field(
        foreign_key="repository.id", description="ID do repositório associado."
    )
    sha1: str = Field(description="SHA1 do commit associado à tag.")
    repository: Repository = Relationship(back_populates="tags")


class RepositoryConfig(SQLModel, table=True):
    """Tabela que representa configurações associadas a um repositório."""

    __table_args__ = {"comment": "Conjunto de Configs especializadas do Repo"}

    id: int | None = Field(
        default=None,
        primary_key=True,
        description="ID único da configuração do repositório.",
    )
    repository_id: int = Field(
        foreign_key="repository.id", description="ID do repositório associado."
    )
    name: str = Field(description="Nome da configuração.")
    spec: Optional[dict] = Field(
        default={},
        sa_column=Column(JSON),
        description="Especificação da configuração em formato JSONB.",
    )
    repository: Repository = Relationship(back_populates="configs")

    def get_config(self, key: str, session):
        """Obtém o valor de uma configuração pela chave, retornando o valor padrão se não existir."""
        if self.spec and key in self.spec:
            return self.spec.get(key)

        # Buscar configuração padrão
        default_config = (
            session.query(DefaultConfig).filter(DefaultConfig.name == key).first()
        )
        return default_config.value if default_config else None

    def set_config(self, key: str, value: Any):
        """Define o valor de uma configuração pela chave."""
        if not self.spec:
            self.spec = {}
        self.spec[key] = value


class DefaultConfig(SQLModel, table=True):
    __table_args__ = {
        "comment": "Configurações padrão usadas na ausência de configurações específicas"
    }

    id: int | None = Field(
        default=None, primary_key=True, description="ID único da configuração padrão."
    )
    name: str = Field(description="Nome da configuração padrão.")

    value: Optional[dict] = Field(
        default={},
        sa_column=Column(JSON),
        description="Valor padrão da configuração.",
    )
