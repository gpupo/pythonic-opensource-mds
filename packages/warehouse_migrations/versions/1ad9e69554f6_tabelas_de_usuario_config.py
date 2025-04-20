"""Tabelas de usuario, config

Revision ID: 1ad9e69554f6
Revises: 56176b90f9b4
Create Date: 2025-04-19 17:39:00.759658

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1ad9e69554f6"
down_revision: Union[str, None] = "56176b90f9b4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade datawarehouse schema."""
    op.create_table(
        "defaultconfig",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("value", sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "profile",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["auth.users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "profileorglink",
        sa.Column("profile_id", sa.Uuid(), nullable=False),
        sa.Column("org_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["org_id"],
            ["org.id"],
        ),
        sa.ForeignKeyConstraint(
            ["profile_id"],
            ["profile.id"],
        ),
        sa.PrimaryKeyConstraint("profile_id", "org_id"),
    )
    op.create_table(
        "repositoryconfig",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("repository_id", sa.Integer(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("spec", sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(
            ["repository_id"],
            ["repository.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.add_column("org", sa.Column("revoked_at", sa.DateTime(), nullable=True))
    op.add_column("product", sa.Column("revoked_at", sa.DateTime(), nullable=True))

    sql = """
    -- Atualizar descrição da tabela Tag
COMMENT ON TABLE tag IS 'Tabela que armazena tags associadas a repositórios.';
COMMENT ON COLUMN tag.id IS 'Identificador único da tag.';
COMMENT ON COLUMN tag.type IS 'Tipo da tag.';
COMMENT ON COLUMN tag.start_date IS 'Data de início da tag.';
COMMENT ON COLUMN tag.end_date IS 'Data de término da tag.';
COMMENT ON COLUMN tag.year IS 'Ano associado à tag.';
COMMENT ON COLUMN tag.number IS 'Número associado à tag.';

-- Atualizar descrição da tabela ProfileOrgLink
COMMENT ON TABLE profileorglink IS 'Tabela de associação.';

-- Atualizar descrição da tabela Org
COMMENT ON TABLE org IS 'Tabela que representa uma organização.';
COMMENT ON COLUMN org.id IS 'ID único da organização.';
COMMENT ON COLUMN org.login IS 'Login da organização.';
COMMENT ON COLUMN org.name IS 'Nome da organização.';
COMMENT ON COLUMN org.url IS 'URL associada à organização.';
COMMENT ON COLUMN org.image IS 'Imagem representativa da organização.';
COMMENT ON COLUMN org.description IS 'Descrição da organização.';
COMMENT ON COLUMN org.revoked_at IS 'Data de revogação da organização.';

-- Atualizar descrição da tabela Profile
COMMENT ON TABLE profile IS 'Tabela atualizada por trigger no login.';
COMMENT ON COLUMN profile.id IS 'ID único do perfil.';

-- Atualizar descrição da tabela Product
COMMENT ON TABLE product IS 'Tabela que representa um produto.';
COMMENT ON COLUMN product.id IS 'ID único do produto.';
COMMENT ON COLUMN product.org_id IS 'ID da organização associada ao produto.';
COMMENT ON COLUMN product.name IS 'Nome do produto.';
COMMENT ON COLUMN product.description IS 'Descrição do produto.';
COMMENT ON COLUMN product.revoked_at IS 'Data de revogação do produto.';

-- Atualizar descrição da tabela Repository
COMMENT ON TABLE repository IS 'Tabela que representa um repositório git de um componente do produto.';
COMMENT ON COLUMN repository.id IS 'ID único do repositório.';
COMMENT ON COLUMN repository.product_id IS 'ID do produto associado ao repositório.';
COMMENT ON COLUMN repository.name IS 'Nome do repositório.';
COMMENT ON COLUMN repository.description IS 'Descrição do repositório.';
COMMENT ON COLUMN repository.url IS 'URL do repositório.';
COMMENT ON COLUMN repository.branch_production IS 'Branch de produção do repositório.';

-- Atualizar descrição da tabela RepositoryTag
COMMENT ON TABLE repositorytag IS 'Tabela que armazena o SHA1 do commit do repositório para cada tag existente.';
COMMENT ON COLUMN repositorytag.id IS 'Identificador único da tag do repositório.';
COMMENT ON COLUMN repositorytag.type IS 'Tipo da tag.';
COMMENT ON COLUMN repositorytag.start_date IS 'Data de início da tag.';
COMMENT ON COLUMN repositorytag.end_date IS 'Data de término da tag.';
COMMENT ON COLUMN repositorytag.repository_id IS 'ID do repositório associado.';
COMMENT ON COLUMN repositorytag.sha1 IS 'SHA1 do commit associado à tag.';

-- Atualizar descrição da tabela RepositoryConfig
COMMENT ON TABLE repositoryconfig IS 'Tabela que representa configurações associadas a um repositório.';
COMMENT ON COLUMN repositoryconfig.id IS 'ID único da configuração do repositório.';
COMMENT ON COLUMN repositoryconfig.repository_id IS 'ID do repositório associado.';
COMMENT ON COLUMN repositoryconfig.name IS 'Nome da configuração.';
COMMENT ON COLUMN repositoryconfig.spec IS 'Especificação da configuração em formato JSONB.';

-- Atualizar descrição da tabela DefaultConfig
COMMENT ON TABLE defaultconfig IS 'Tabela que representa configurações padrão usadas na ausência de configurações específicas.';
COMMENT ON COLUMN defaultconfig.id IS 'ID único da configuração padrão.';
COMMENT ON COLUMN defaultconfig.name IS 'Nome da configuração padrão.';
COMMENT ON COLUMN defaultconfig.value IS 'Valor padrão da configuração.';

    """

    op.execute(sql)


# ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade datawarehouse schema."""
    op.drop_column("product", "revoked_at")
    op.drop_column("org", "revoked_at")
    op.drop_table("repositoryconfig")
    op.drop_table("profileorglink")
    op.drop_table("profile")
    op.drop_table("defaultconfig")
    # ### end Alembic commands ###
