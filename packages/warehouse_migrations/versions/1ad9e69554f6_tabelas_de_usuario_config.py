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
