"""visibilidade-public

Revision ID: 41f736a2b497
Revises: 1ad9e69554f6
Create Date: 2025-04-20 06:42:54.428110

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "41f736a2b497"
down_revision: Union[str, None] = "1ad9e69554f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade datawarehouse schema."""
    op.create_table_comment(
        "defaultconfig",
        "Configurações padrão usadas na ausência de configurações específicas",
        existing_comment="Tabela que representa configurações padrão usadas na ausência de configurações específicas.",
        schema=None,
    )
    op.add_column(
        "org",
        sa.Column(
            "is_public",
            sa.Boolean(),
            nullable=True,
            comment="Define se a visibilidade é pública.",
        ),
    )
    op.execute("UPDATE org SET is_public = false")
    op.alter_column("org", "is_public", nullable=False)

    op.add_column(
        "product",
        sa.Column(
            "is_public",
            sa.Boolean(),
            nullable=False,
            comment="Define se a visibilidade é pública.",
        ),
    )
    op.create_table_comment(
        "product",
        "Produto de Software que aninha componentes",
        existing_comment="Tabela que representa um produto.",
        schema=None,
    )
    op.alter_column(
        "profile",
        "id",
        existing_type=sa.UUID(),
        comment=None,
        existing_comment="ID único do perfil.",
        existing_nullable=False,
    )
    op.create_table_comment(
        "profile",
        "Perfil de usuarios",
        existing_comment="Tabela atualizada por trigger no login.",
        schema=None,
    )
    op.alter_column(
        "profileorglink",
        "profile_id",
        existing_type=sa.UUID(),
        comment="ID do perfil",
        existing_nullable=False,
    )
    op.alter_column(
        "profileorglink",
        "org_id",
        existing_type=sa.INTEGER(),
        comment="ID da organização",
        existing_nullable=False,
    )
    op.create_table_comment(
        "profileorglink",
        "Table pivot",
        existing_comment="Tabela de associação.",
        schema=None,
    )
    op.add_column(
        "repository",
        sa.Column(
            "is_public",
            sa.Boolean(),
            nullable=False,
            comment="Define se a visibilidade é pública.",
        ),
    )
    op.create_table_comment(
        "repository",
        "Repo Git-Based de um componente",
        existing_comment="Tabela que representa um repositório git de um componente do produto.",
        schema=None,
    )
    op.create_table_comment(
        "repositoryconfig",
        "Conjunto de Configs especializadas do Repo",
        existing_comment="Tabela que representa configurações associadas a um repositório.",
        schema=None,
    )
    op.create_table_comment(
        "repositorytag",
        "Tags sobre commits do repo git-based",
        existing_comment="Tabela que armazena o SHA1 do commit do repositório para cada tag existente.",
        schema=None,
    )
    op.create_table_comment(
        "tag",
        "Tabela de tags do sistema",
        existing_comment="Tabela que armazena tags associadas a repositórios.",
        schema=None,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade datawarehouse schema."""
    op.create_table_comment(
        "tag",
        "Tabela que armazena tags associadas a repositórios.",
        existing_comment="Tabela de tags do sistema",
        schema=None,
    )
    op.create_table_comment(
        "repositorytag",
        "Tabela que armazena o SHA1 do commit do repositório para cada tag existente.",
        existing_comment="Tags sobre commits do repo git-based",
        schema=None,
    )
    op.create_table_comment(
        "repositoryconfig",
        "Tabela que representa configurações associadas a um repositório.",
        existing_comment="Conjunto de Configs especializadas do Repo",
        schema=None,
    )
    op.create_table_comment(
        "repository",
        "Tabela que representa um repositório git de um componente do produto.",
        existing_comment="Repo Git-Based de um componente",
        schema=None,
    )
    op.drop_column("repository", "is_public")
    op.create_table_comment(
        "profileorglink",
        "Tabela de associação.",
        existing_comment="Table pivot",
        schema=None,
    )
    op.alter_column(
        "profileorglink",
        "org_id",
        existing_type=sa.INTEGER(),
        comment=None,
        existing_comment="ID da organização",
        existing_nullable=False,
    )
    op.alter_column(
        "profileorglink",
        "profile_id",
        existing_type=sa.UUID(),
        comment=None,
        existing_comment="ID do perfil",
        existing_nullable=False,
    )
    op.create_table_comment(
        "profile",
        "Tabela atualizada por trigger no login.",
        existing_comment="Perfil de usuarios",
        schema=None,
    )
    op.alter_column(
        "profile",
        "id",
        existing_type=sa.UUID(),
        comment="ID único do perfil.",
        existing_nullable=False,
    )
    op.create_table_comment(
        "product",
        "Tabela que representa um produto.",
        existing_comment="Produto de Software que aninha componentes",
        schema=None,
    )
    op.drop_column("product", "is_public")
    op.drop_column("org", "is_public")
    op.create_table_comment(
        "defaultconfig",
        "Tabela que representa configurações padrão usadas na ausência de configurações específicas.",
        existing_comment="Configurações padrão usadas na ausência de configurações específicas",
        schema=None,
    )
    # ### end Alembic commands ###
